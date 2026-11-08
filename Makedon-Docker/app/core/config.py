

'''
@lru_cache делает так, что функция реально выполнится только один раз за всё время работы приложения — 
при первом вызове создаст объект, а при всех следующих вызовах просто вернёт тот же самый, уже готовый объект, 
не создавая новый каждый раз. Это стандартный паттерн в FastAPI-проектах для конфигурации (его даже в официальной 
документации FastAPI именно так и показывают).
'''


from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    cors_allowed_origins: list[str]


@lru_cache
def get_settings() -> Settings:
    return Settings(
        DATABASE_URL="postgresql+psycopg://postgres:admin@postgres:5432/postgres",
        cors_allowed_origins=["http://localhost:8080"],
    )