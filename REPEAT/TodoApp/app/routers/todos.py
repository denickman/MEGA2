# routers/todos.py — CRUD-эндпоинты для задач

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from app.core.security import get_current_user
from app.database import db_dependency
from app.models import Todos
from app.schemas.todo import TodoRequest

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, user: user_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail="auth failed")

    return db.query(Todos).filter(Todos.owner_id == user.get("user_id")).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail="auth failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="todo not found")
    return todo_model


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, user: user_dependency, todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=401, detail="auth failed")

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("user_id"))
    db.add(todo_model)
    db.commit()


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency,
    user: user_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="auth failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
    ).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed

    db.add(todo_model)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail="auth failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=404, detail="todo not found")

    db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get("user_id")
    ).delete()
    db.commit()

    # db.delete(todo_model)
    # db.commit()
