from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import models
from database import get_db
from schemas import PostResponse, UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/api/users", tags=["users"])

## create_user (POST)
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    # Проверяем, нет ли уже пользователя с таким username или email
    result = await db.execute(
        select(models.User).where(
            (models.User.username == user.username) | (models.User.email == user.email)
        )
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    new_user = models.User(
        username=user.username,
        email=user.email,
        image_file=user.image_file,  # None, если не передали
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


## get_user_posts (GET) — посты конкретного пользователя
@router.get("/{user_id}/posts", response_model=list[PostResponse])
async def get_user_posts(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.user_id == user_id),
    )
    posts = result.scalars().all()
    return posts


## update_user_full (PUT)
@router.put("/{user_id}", response_model=UserResponse)
async def update_user_full(
    user_id: int,
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = await db.execute(
        select(models.User).where(
            models.User.id != user_id,
            or_(
                models.User.username == user_data.username,
                models.User.email == user_data.email,
            ),
        )
    )
    existing = result.scalars().first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    user.username = user_data.username
    user.email = user_data.email
    user.image_file = user_data.image_file  # PUT = полная замена: не передали -> сброс в None

    await db.commit()
    await db.refresh(user)
    return user


## update_user_partial (PATCH)
@router.patch("/{user_id}", response_model=UserResponse)
async def update_user_partial(
    user_id: int,
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Берём только присланные поля. None оставляем лишь для image_file:
    # {"image_file": null} убирает картинку. Для username и email (NOT NULL в БД)
    # null игнорируем.
    update_data = user_data.model_dump(exclude_unset=True)
    for field in ("username", "email"):
        if update_data.get(field) is None:
            update_data.pop(field, None)

    conditions = []
    if "username" in update_data:
        conditions.append(models.User.username == update_data["username"])
    if "email" in update_data:
        conditions.append(models.User.email == update_data["email"])

    if conditions:
        result = await db.execute(
            select(models.User).where(
                models.User.id != user_id,
                or_(*conditions),
            )
        )
        existing = result.scalars().first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists",
            )

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


## delete_user (DELETE)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await db.delete(user)  # в async delete тоже нужен await
    await db.commit()