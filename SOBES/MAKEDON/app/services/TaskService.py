from sqlalchemy.orm import Session

from app.repos.TaskRepository import TaskRepository
from app.schemas.TaskSchema import TaskSchema, TaskCreateSchema, TaskUpdateSchema


class TaskNotFound(Exception):
    """
    Task does not exist
    """


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repo = TaskRepository(db)

    def list_tasks(self) -> list[TaskSchema]:
        tasks_orm = self.task_repo.get_all_tasks()
        return [TaskSchema.model_validate(task) for task in tasks_orm]

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task = self.task_repo.create_task(title=task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task)

    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        task_for_update = self.task_repo.get_task_by_id(task_id=task_id)
        if not task_for_update:
            raise TaskNotFound(f'Task with id {task_id} not found')
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed
        self.db.commit()
        return TaskSchema.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> None:
        task_for_delete = self.task_repo.get_task_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f'Task with id {task_id} not found')
        self.task_repo.delete_task(task_for_delete)
        self.db.commit()