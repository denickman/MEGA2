from pydantic import BaseModel, Field
from sqlalchemy.sql.annotation import Annotated
from starlette import status
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path

from database import db_dependency
from models import Todos
from .auth import get_current_user

router = APIRouter()
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool


@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, user: user_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail='auth failed')

    return db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()


@router.get('/todos/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='auth failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
                  .filter(Todos.owner_id == user.get('user_id'))\
                  .first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')
    return todo_model


@router.post('/todos', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, user: user_dependency, todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=401, detail='auth failed')

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('user_id'))
    db.add(todo_model)
    db.commit()

@router.put('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, user: user_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='auth failed')

    todo_model = (db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id'))).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed

    db.add(todo_model)
    db.commit()


@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='auth failed')

    todo_model = (db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first())

    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')

    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).delete()
    db.commit()

    # db.delete(todo_model)
    # db.commit()