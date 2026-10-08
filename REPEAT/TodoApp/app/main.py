# main.py — точка входа FastAPI-приложения
# Запуск: uvicorn app.main:app --reload

from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import auth, todos, users, admin

app = FastAPI()

# Подключаем роутеры (каждый — отдельный файл с эндпоинтами)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)
# FIX: убран дубликат auth.router, добавлен admin.router

# Создаёт таблицы в БД при первом запуске (если их ещё нет)
# Не изменяет уже существующие таблицы — для этого нужен Alembic
models.Base.metadata.create_all(bind=engine)
