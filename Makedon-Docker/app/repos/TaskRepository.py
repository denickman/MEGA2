from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.task import TaskORM


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_tasks(self) -> list[TaskORM]:
        return self.db.scalars(select(TaskORM)).all()

    def get_task_by_id(self, task_id: str) -> TaskORM | None:
        return self.db.get(TaskORM, task_id)

    def create_task(self, title: str) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        return new_task

    def delete_task(self, task: TaskORM) -> None:
        self.db.delete(task)