# config.py — настройки приложения через pydantic-settings
# Все секреты читаются из файла .env (который лежит в корне проекта)
# pip install pydantic-settings

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения.
    Значения берутся из переменных окружения или из файла .env.
    Имена полей (в lowercase) должны совпадать с ключами в .env (case-insensitive).
    """

    # JWT
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 20

    # База данных
    database_url: str = "sqlite:///./todosapp.db"

    class Config:
        env_file = ".env"


# Единственный экземпляр настроек — импортируй его откуда нужно
settings = Settings()
