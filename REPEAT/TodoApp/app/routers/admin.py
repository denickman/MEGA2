# routers/admin.py — эндпоинты только для администраторов

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from app.core.security import get_current_user
from app.database import db_dependency
from app.models import Todos

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

user_dependency = Annotated[dict, Depends(get_current_user)]



@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    # FIX: было user.get("role") — неправильный ключ!
    # Правильно: user.get("user_role")
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Not authorized. Admin access required.")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="todo not found")

    db.delete(todo_model)
    db.commit()
