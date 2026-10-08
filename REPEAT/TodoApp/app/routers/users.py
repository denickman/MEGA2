# routers/users.py — профиль пользователя, смена пароля и телефона

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.security import bcrypt_context, get_current_user
from app.database import db_dependency
from app.models import Users
from app.schemas.user import UserVerification, UserResponse, PhoneNumberRequest

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def index(user: user_dependency, db: db_dependency):
    """
    Получить профиль текущего пользователя.
    response_model=UserResponse гарантирует, что hashed_password
    НЕ попадёт в ответ — Pydantic отфильтрует лишние поля.
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return db.query(Users).filter(Users.id == user.get("user_id")).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phone", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user: user_dependency,
    db: db_dependency,
    request: PhoneNumberRequest,
):
    """
    Смена номера телефона.
    Номер передаётся в теле запроса (JSON), а НЕ в URL —
    так безопаснее и правильнее по REST.
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_model.phone_number = request.phone_number
    db.add(user_model)
    db.commit()
