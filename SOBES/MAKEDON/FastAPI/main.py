from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from starlette import status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column


# lifespan for fastapi
@asynccontextmanager
async def lifespan(_: FastAPI):
    # create tables
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

# просмотр таблиц - docker exec -it b9897c1e5892 psql -U postgres -d postgres -c "\dt"
DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker[Session](bind=engine)

# Base model
class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)









class TaskSchema(BaseModel):
   id: str
   title: str
   completed: bool


class TaskCreateSchema(BaseModel):
   title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None




app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks: list[TaskSchema] = [

]



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def task_orm_to_model(task_orm :TaskORM) -> TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)















# @app.get("/")
# def read_base_page():
#     return {"message": "World"}


@app.get('/tasks')
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in tasks_from_db]


@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    # new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    # tasks.append(new_task)

    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()
    return task_orm_to_model(new_task)



@app.patch('/tasks/{task_id}')
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    # for task in tasks:
    #     if task.id == task_id:
    #         if payload.title:
    #             task.title = payload.title
    #         if payload.completed is not None:
    #             task.completed = payload.completed
    #         return task


    task_for_update = db.get(TaskORM, task_id)
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed is not None:
        task_for_update.completed = payload.completed

    db.commit()
    return task_orm_to_model(task_for_update)




@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    # for task in tasks:
    #     if task.id == task_id:
    #         tasks.remove(task)

    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()












