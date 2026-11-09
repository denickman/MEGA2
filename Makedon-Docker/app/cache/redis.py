"""
Низкоуровневый кэш-бэкенд: "положи/достань любой JSON-совместимый объект по ключу".

Про типы ничего не знает — ни про задачи, ни про Pydantic. Это сознательно:
такой класс переиспользуется для любых данных.
"""

import json
import logging
from functools import lru_cache
from typing import Any

from redis import Redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)


@lru_cache
def get_redis_client(redis_url: str) -> Redis:
    """
    Один клиент (и один пул соединений) на весь процесс.

    Важно: Redis.from_url() создаёт пул TCP-соединений. Если вызывать его на
    каждый HTTP-запрос, пулы будут плодиться и течь. @lru_cache по URL даёт
    singleton.
    """
    return Redis.from_url(redis_url, decode_responses=True)


class RedisCacheBackend:
    def __init__(self, redis_client: Redis, cache_ttl_seconds: int | None = None) -> None:
        self.redis = redis_client
        self.cache_ttl_seconds = cache_ttl_seconds

    def get(self, key: str) -> Any | None:
        """
        None означает "в кэше ничего нет" — вызывающий код должен идти в БД.

        Ошибка Redis тоже отдаёт None (fail-open): кэш — это ускоритель, а не
        источник правды, поэтому упавший Redis не должен ломать весь API.
        """
        try:
            raw = self.redis.get(key)
        except RedisError:
            logger.warning("cache read failed for key=%s, falling back to DB", key, exc_info=True)
            return None

        if raw is None:
            return None

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # В ключе лежит мусор (например, формат поменялся между деплоями).
            logger.warning("cache value for key=%s is not valid JSON, dropping it", key)
            self.delete(key)
            return None

    def set(self, key: str, value: Any) -> None:
        """Не смогли записать в кэш — это не причина ломать ответ клиенту."""
        try:
            self.redis.set(key, json.dumps(value), ex=self.cache_ttl_seconds)
        except RedisError:
            logger.warning("cache write failed for key=%s", key, exc_info=True)

    def delete(self, key: str) -> None:
        """
        А вот здесь ошибку НЕ глотаем, и это главное отличие от get/set.

        Неудачное чтение кэша стоит нам лишнего запроса в БД — неприятно, но
        безопасно. Неудачная инвалидация оставляет в кэше устаревшие данные на
        весь TTL, и клиенты будут видеть неправду. Лучше вернуть 500 на запись,
        чем молча отдавать протухший список.
        """
        self.redis.delete(key)
