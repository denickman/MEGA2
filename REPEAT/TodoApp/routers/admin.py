from pydantic import BaseModel, Field
from sqlalchemy.sql.annotation import Annotated
from starlette import status
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path

from database import db_dependency
from models import Todos
from .auth import get_current_user





router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

user_dependency = Annotated[dict,Depends(get_current_user)]



@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get("id") != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return db.query(Todos).all()


@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get("role") != 'admin':
        raise HTTPException(status_code=401, detail='Incorrect username or password')

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')

    db.delete(todo_model)
    db.commit()
















