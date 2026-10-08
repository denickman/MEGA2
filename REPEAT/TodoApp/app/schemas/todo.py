# schemas/todo.py — Pydantic-схемы для задач (todos)

from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    """Схема для создания/обновления задачи"""
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool
