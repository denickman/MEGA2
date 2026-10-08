from passlib.handlers.bcrypt import bcrypt
from pydantic import BaseModel, Field
from sqlalchemy.sql.annotation import Annotated
from starlette import status
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path

from database import db_dependency
from models import Todos, Users
from .auth import get_current_user

from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)




@router.get('/', status_code=status.HTTP_200_OK)
async def index(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    return db.query(Users).filter(Users.id == user.get("user_id")).first()


@router.put('/', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()







