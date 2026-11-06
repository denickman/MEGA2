


from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status
from fastapi.middleware.cors import CORSMiddleware


class TaskSchema(BaseModel):
   id: str
   title: str
   completed: bool


class TaskCreateSchema(BaseModel):
   title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks: list[TaskSchema] = [

]


# @app.get("/")
# def read_base_page():
#     return {"message": "World"}


@app.get('/tasks')
def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)
    return new_task



@app.patch('/tasks/{task_id}')
def update_task(task_id: str, payload: TaskUpdateSchema):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task



@app.delete('/tasks/{id}')
def delete_task(task_id: str, status_code=status.HTTP_204_NO_CONTENT):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)












