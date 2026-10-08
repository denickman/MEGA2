# schemas/auth.py — Pydantic-схемы для регистрации и аутентификации

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    """Схема для создания нового пользователя (POST /auth/auth)"""
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class Token(BaseModel):
    """Схема ответа при логине — содержит JWT-токен"""
    access_token: str
    token_type: str
