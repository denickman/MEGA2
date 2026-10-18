from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

import models
from database import Base, engine, get_db
from schemas import (
    PostCreate,
    PostResponse,
    PostUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)


# =============================================================================
# APP SETUP
# =============================================================================

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")


# =============================================================================
# HTML PAGES (скрыты из Swagger)
# =============================================================================

## home
@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )


## post_page
@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        title = post.title[:50]
        return templates.TemplateResponse(
            request,
            "post.html",
            {"post": post, "title": title},
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


## user_posts_page
@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
def user_posts_page(
    request: Request,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )


# =============================================================================
# USERS API   (/api/users)
# =============================================================================

## create_user (POST)
@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    # Проверяем, нет ли уже пользователя с таким username или email
    result = db.execute(
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
    db.commit()
    db.refresh(new_user)
    return new_user


## get_user_posts (GET) — посты конкретного пользователя
@app.get("/api/users/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return posts


## update_user_full (PUT)
@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user_full(
    user_id: int,
    user_data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    user = db.execute(
        select(models.User).where(models.User.id == user_id)
    ).scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    existing = db.execute(
        select(models.User).where(
            models.User.id != user_id,
            or_(
                models.User.username == user_data.username,
                models.User.email == user_data.email,
            ),
        )
    ).scalars().first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    user.username = user_data.username
    user.email = user_data.email
    user.image_file = user_data.image_file  # PUT = полная замена: не передали -> сброс в None

    db.commit()
    db.refresh(user)
    return user


## update_user_partial (PATCH)
@app.patch("/api/users/{user_id}", response_model=UserResponse)
def update_user_partial(
    user_id: int,
    user_data: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    user = db.execute(
        select(models.User).where(models.User.id == user_id)
    ).scalars().first()

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
        existing = db.execute(
            select(models.User).where(
                models.User.id != user_id,
                or_(*conditions),
            )
        ).scalars().first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists",
            )

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


## delete_user (DELETE)
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(
        select(models.User).where(models.User.id == user_id)
    ).scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    db.delete(user)
    db.commit()


# =============================================================================
# POSTS API   (/api/posts)
# =============================================================================

## create_post (POST)
@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == post.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


## get_posts (GET, список)
@app.get("/api/posts", response_model=list[PostResponse])
def get_posts(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts


## get_post (GET, один)
@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


## update_post_full (PUT)
@app.put("/api/posts/{post_id}", response_model=PostResponse)
def update_post_full(
    post_id: int,
    post_data: PostCreate,
    db: Annotated[Session, Depends(get_db)],
):
    post = db.execute(
        select(models.Post).where(models.Post.id == post_id)
    ).scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if post_data.user_id != post.user_id:
        user = db.execute(
            select(models.User).where(models.User.id == post_data.user_id)
        ).scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    post.title = post_data.title
    post.content = post_data.content
    post.user_id = post_data.user_id

    db.commit()
    db.refresh(post)
    return post


## update_post_partial (PATCH)
@app.patch("/api/posts/{post_id}", response_model=PostResponse)
def update_post_partial(
    post_id: int,
    post_data: PostUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    post = db.execute(
        select(models.Post).where(models.Post.id == post_id)
    ).scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    update_data = post_data.model_dump(exclude_unset=True, exclude_none=True)

    for field, value in update_data.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


## delete_post (DELETE)
@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = db.execute(
        select(models.Post).where(models.Post.id == post_id)
    ).scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    db.delete(post)
    db.commit()


# =============================================================================
# EXCEPTION HANDLERS
# =============================================================================

## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


#
# ### RequestValidationError Handler
# @app.exception_handler(RequestValidationError)
# def validation_exception_handler(request: Request, exception: RequestValidationError):
#     if request.url.path.startswith("/api"):
#         return JSONResponse(
#             status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
#             content={"detail": exception.errors()},
#         )
#     return templates.TemplateResponse(
#         request,
#         "error.html",
#         {
#             "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
#             "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
#             "message": "Invalid request. Please check your input and try again.",
#         },
#         status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
#     )