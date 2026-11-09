import logging
from time import perf_counter

from sqlalchemy.orm import Session

from app.cache.TasksCache import TasksCache
from app.repos.TaskRepository import TaskRepository
from app.schemas.TaskRead import TaskRead, TaskCreateSchema, TaskUpdateSchema

logger = logging.getLogger(__name__)


class TaskNotFound(Exception):
    """
    Task does not exist
    """


class TaskService:
    def __init__(self, db: Session, tasks_cache: TasksCache) -> None:
        self.db = db
        self.task_repo = TaskRepository(db)
        self.cache = tasks_cache
        # "HIT" / "MISS" последнего чтения — роутер выставит это в заголовок ответа,
        # чтобы в Swagger было видно, откуда пришли данные.
        self.last_cache_status: str = "N/A"

    def list_tasks(self) -> list[TaskRead]:
        start_time = perf_counter()

        cached_tasks = self.cache.get_tasks()
        if cached_tasks is not None:
            self.last_cache_status = "HIT"
            logger.info(
                "tasks list served from CACHE in %.2f ms (%d items)",
                (perf_counter() - start_time) * 1000,
                len(cached_tasks),
            )
            return cached_tasks

        self.last_cache_status = "MISS"
        tasks_orm = self.task_repo.get_all_tasks()
        tasks_read = [TaskRead.model_validate(task) for task in tasks_orm]
        self.cache.set_tasks(tasks_read)

        logger.info(
            "tasks list served from DB in %.2f ms (%d items)",
            (perf_counter() - start_time) * 1000,
            len(tasks_read),
        )
        return tasks_read

    def create_task(self, task_create: TaskCreateSchema) -> TaskRead:
        task = self.task_repo.create_task(title=task_create.title)
        self.db.commit()
        result = TaskRead.model_validate(task)

        # Инвалидация ПОСЛЕ успешного commit: пока транзакция не зафиксирована,
        # сбрасывать кэш рано — если commit упадёт, мы выбросим валидный кэш зря,
        # а в худшем случае параллельный GET успеет перезаписать его ещё не
        # закоммиченным (то есть несуществующим) состоянием.
        self.cache.invalidate()
        return result

    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskRead:
        task_for_update = self.task_repo.get_task_by_id(task_id=task_id)
        if not task_for_update:
            # Ничего не меняли — кэш трогать не за что.
            raise TaskNotFound(f'Task with id {task_id} not found')

        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        self.db.commit()
        result = TaskRead.model_validate(task_for_update)

        self.cache.invalidate()
        return result

    def delete_task(self, task_id: str) -> None:
        task_for_delete = self.task_repo.get_task_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f'Task with id {task_id} not found')

        self.task_repo.delete_task(task_for_delete)
        self.db.commit()

        self.cache.invalidate()
