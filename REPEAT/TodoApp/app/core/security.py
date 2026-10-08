# security.py — всё, что связано с аутентификацией и безопасностью
# bcrypt для хеширования паролей, JWT для токенов, OAuth2 схема

from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from app.core.config import settings


# === Хеширование паролей (bcrypt) ===
# CryptContext — обёртка passlib, которая умеет хешировать и проверять пароли
# schemes=["bcrypt"] — используем алгоритм bcrypt
# deprecated="auto" — если добавим другой алгоритм, старые хеши автоматически пометятся устаревшими
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === OAuth2 схема ===
# tokenUrl — путь, куда Swagger будет отправлять логин/пароль для получения токена
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    """
    Создаёт JWT-токен.
    Внутри токена (payload) зашиты: username, user_id, role и срок жизни.
    """
    encode = {
        "sub": username,
        "id": user_id,
        "role": role,
    }

    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Dependency для защищённых эндпоинтов.
    Берёт токен из заголовка Authorization: Bearer <token>,
    декодирует его и возвращает dict с данными пользователя.
    Если токен невалидный — бросает 401.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Credentials",
            )
        return {"username": username, "user_id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
        )
