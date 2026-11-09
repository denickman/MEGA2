"""
Кэш конкретно для списка задач.

Этот класс — ответ на вопрос "куда девать кучу cache_* параметров в сервисе".
Он знает ровно три вещи, которые раньше болтались в TaskService по отдельности:
  - какой backend использовать,
  - под каким ключом лежат задачи,
  - в каком виде они там лежат (dict <-> TaskRead).

TaskService после этого не знает ни про ключи, ни про JSON — он просто
спрашивает "задачи есть?" и говорит "сбрось".
"""

from app.cache.redis import RedisCacheBackend
from app.schemas.TaskRead import TaskRead


class TasksCache:
    def __init__(self, backend: RedisCacheBackend, key: str) -> None:
        self._backend = backend
        self._key = key

    def get_tasks(self) -> list[TaskRead] | None:
        """None = промах кэша (в нём ничего нет). Пустой список = в БД реально 0 задач."""
        cached = self._backend.get(self._key)
        if cached is None:
            return None
        return [TaskRead.model_validate(item) for item in cached]

    def set_tasks(self, tasks: list[TaskRead]) -> None:
        self._backend.set(self._key, [task.model_dump() for task in tasks])

    def invalidate(self) -> None:
        self._backend.delete(self._key)
