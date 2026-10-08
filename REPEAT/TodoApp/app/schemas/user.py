# schemas/user.py — Pydantic-схемы для профиля пользователя

from pydantic import BaseModel, Field


class UserVerification(BaseModel):
    """Схема для смены пароля — текущий пароль + новый"""
    password: str
    new_password: str = Field(min_length=6)


class UserResponse(BaseModel):
    """
    Схема ответа — данные пользователя БЕЗ хеша пароля.
    Используется как response_model, чтобы hashed_password
    никогда не попадал в JSON-ответ API.
    """
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    role: str
    phone_number: str | None = None

    class Config:
        from_attributes = True  # чтобы Pydantic мог читать ORM-объекты


class PhoneNumberRequest(BaseModel):
    """Схема для смены номера телефона (через тело запроса, а не URL)"""
    phone_number: str
