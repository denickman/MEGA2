import logging
import time
from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from app.api.routers.TaskRouter import router as task_router
from app.core.config import get_settings
from app.db.session import engine
from app.models.base import Base

# Без этого logger.info(...) из сервисов и кэша никуда не попадёт:
# uvicorn настраивает только свои логгеры, а корневой остаётся на WARNING.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()


def create_tables_with_retry(attempts: int = 10, delay_seconds: float = 1.5) -> None:
    """
    При ручном docker run контейнер приложения часто стартует раньше, чем
    Postgres успевает принять соединения. Вместо падения — несколько попыток.
    """
    for attempt in range(1, attempts + 1):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("tables are ready")
            return
        except OperationalError:
            logger.warning("database is not ready (attempt %d/%d), retrying...", attempt, attempts)
            time.sleep(delay_seconds)
    raise RuntimeError("database is not reachable, giving up")


# lifespan for fastapi
@asynccontextmanager
async def lifespan(_: FastAPI):
    # create tables
    create_tables_with_retry()
    yield


app = FastAPI(lifespan=lifespan, title="Tasks API")
app.include_router(router=task_router)


@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    """
    Замер полного времени обработки запроса.

    Результат уезжает в заголовок X-Process-Time-Ms, который Swagger UI
    показывает в блоке Response headers. Плюс строчка в логах — её видно
    в `docker logs -f tasks-app`.
    """
    start = perf_counter()
    response = await call_next(request)
    elapsed_ms = (perf_counter() - start) * 1000

    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
    logger.info(
        "%s %s -> %d | %.2f ms | cache=%s",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
        response.headers.get("X-Cache", "-"),
    )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Без этого браузерный фронтенд на другом origin не сможет прочитать
    # наши кастомные заголовки из JS (Swagger на том же origin увидит их и так).
    expose_headers=["X-Cache", "X-Process-Time-Ms"],
)
