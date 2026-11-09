from fastapi import Depends
from sqlalchemy.orm import Session

from app.cache.TasksCache import TasksCache
from app.cache.redis import RedisCacheBackend, get_redis_client
from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.services.TaskService import TaskService


def get_tasks_cache(settings: Settings = Depends(get_settings)) -> TasksCache:
    """
    Собирает кэш списка задач.

    get_redis_client закэширован через @lru_cache, поэтому на каждый запрос
    создаётся только дешёвая обёртка, а не новый пул соединений к Redis.
    """
    backend = RedisCacheBackend(
        redis_client=get_redis_client(settings.redis_url),
        cache_ttl_seconds=settings.cache_ttl_seconds,
    )
    return TasksCache(backend=backend, key=settings.cache_tasks_key)


def get_task_service(
    db: Session = Depends(get_db),
    tasks_cache: TasksCache = Depends(get_tasks_cache),
) -> TaskService:
    """
    method for dep injection

    Сервис больше не конструирует свои зависимости сам — он получает уже
    готовые db и cache. Это и есть dependency injection: сервис не знает, что
    кэш именно в Redis, и его легко подменить в тестах.
    """
    return TaskService(db=db, tasks_cache=tasks_cache)
