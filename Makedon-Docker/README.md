# Tasks API

FastAPI + Postgres + Redis-кэш на списке задач.

## Запуск в Docker вручную (без compose)

См. **RUN-MANUAL.md** — там пошагово сеть, Postgres, Redis, сборка и запуск,
плюс сценарий проверки кэша через Swagger.

## Запуск через compose

```bash
docker compose up --build
```

Swagger: http://127.0.0.1:8000/docs

## Локальный запуск (приложение на хосте, БД и Redis в Docker)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

docker run -d --name tasks-postgres -e POSTGRES_PASSWORD=admin -p 5432:5432 postgres:18-alpine
docker run -d --name tasks-redis -p 6379:6379 redis:8-alpine

uvicorn app.main:app --reload --port 8080
```

Дефолты в `app/core/config.py` рассчитаны ровно на этот случай (`localhost`),
поэтому переменные окружения задавать не нужно.

Swagger: http://127.0.0.1:8080/docs

## Переменные окружения

| Переменная | Дефолт | Назначение |
|---|---|---|
| `DATABASE_URL` | `postgresql+psycopg://postgres:admin@localhost:5432/postgres` | подключение к Postgres |
| `REDIS_URL` | `redis://localhost:6379/0` | подключение к Redis |
| `CACHE_TTL_SECONDS` | `60` | TTL кэша списка задач |
| `CACHE_TASKS_KEY` | `cache:tasks_list` | ключ в Redis |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | origins через запятую |
| `SQL_ECHO` | `0` | `1` — логировать весь SQL |

## Диагностические заголовки ответа

| Заголовок | Значение |
|---|---|
| `X-Cache` | `HIT` — ответ из Redis, `MISS` — из Postgres (только на `GET /tasks`) |
| `X-Process-Time-Ms` | время обработки запроса целиком |

## Полезное

```bash
# таблицы
docker exec -it tasks-postgres psql -U postgres -d postgres -c "\dt"

# содержимое кэша
docker exec -it tasks-redis redis-cli GET cache:tasks_list
docker exec -it tasks-redis redis-cli TTL cache:tasks_list
```
