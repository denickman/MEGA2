"""
Настройки приложения.

@lru_cache делает так, что функция реально выполнится только один раз за всё время
работы приложения — при первом вызове создаст объект, а при всех следующих вызовах
вернёт тот же самый, уже готовый объект. Это стандартный паттерн в FastAPI-проектах
для конфигурации.

Все значения читаются из переменных окружения, а дефолты рассчитаны на ЛОКАЛЬНЫЙ
запуск (localhost). В Docker хосты другие (имена контейнеров), поэтому там
DATABASE_URL / REDIS_URL передаются через -e при docker run.
"""

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    database_url: str
    redis_url: str
    cache_ttl_seconds: int
    cache_tasks_key: str
    cors_allowed_origins: list[str]
    sql_echo: bool


@lru_cache
def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://postgres:admin@localhost:5432/postgres",
        ),
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        cache_ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", "60")),
        cache_tasks_key=os.getenv("CACHE_TASKS_KEY", "cache:tasks_list"),
        cors_allowed_origins=[
            origin.strip()
            for origin in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
            if origin.strip()
        ],
        # SQL-лог по умолчанию выключен: иначе он забивает вывод и в нём
        # не видно собственных логов кэша.
        sql_echo=os.getenv("SQL_ECHO", "0") == "1",
    )
