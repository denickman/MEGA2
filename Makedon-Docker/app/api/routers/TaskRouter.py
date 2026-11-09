from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_task_service
from app.schemas.TaskRead import TaskRead, TaskCreateSchema, TaskUpdateSchema
from app.services.TaskService import TaskService, TaskNotFound


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get('')
def read_tasks(
        response: Response,
        task_service: TaskService = Depends(get_task_service)
) -> list[TaskRead]:
    tasks = task_service.list_tasks()
    # Этот заголовок видно в Swagger в блоке Response headers:
    # MISS — данные пришли из Postgres, HIT — из Redis.
    response.headers["X-Cache"] = task_service.last_cache_status
    return tasks


@router.post('', status_code=status.HTTP_201_CREATED)
def create_task(
        payload: TaskCreateSchema,
        task_service: TaskService = Depends(get_task_service)
) -> TaskRead:
    return task_service.create_task(task_create=payload)


@router.patch('/{task_id}')
def update_task(
        task_id: str,
        payload: TaskUpdateSchema,
        task_service: TaskService = Depends(get_task_service)
) -> TaskRead:
    try:
        return task_service.update_task(task_id=task_id, task_update=payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
        task_id: str,
        task_service: TaskService = Depends(get_task_service)
):
    try:
        task_service.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
