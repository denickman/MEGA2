# Ручной запуск в Docker (без docker compose)

Смысл: вручную сделать всё то, что compose делает за тебя — сеть, три контейнера,
переменные окружения, порты.

## 0. Чистый старт (если что-то уже висит)

```bash
docker rm -f tasks-app tasks-postgres tasks-redis 2>/dev/null
docker network rm tasks-net 2>/dev/null
```

## 1. Сеть

Compose создаёт её сам. Вручную — надо самому. Без общей сети контейнеры не видят
друг друга по имени.

```bash
docker network create tasks-net
```

## 2. Postgres

`--name tasks-postgres` — это ещё и DNS-имя внутри сети `tasks-net`.
`-p 5432:5432` нужен только чтобы ты мог залезть в БД с хоста (если у тебя уже
крутится локальный Postgres на 5432 — поменяй на `-p 5433:5432` или убери флаг).

```bash
docker run -d \
  --name tasks-postgres \
  --network tasks-net \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=postgres \
  -v tasks_pg_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:18-alpine
```

Дождаться готовности:

```bash
until docker exec tasks-postgres pg_isready -U postgres; do sleep 1; done
```

## 3. Redis

```bash
docker run -d \
  --name tasks-redis \
  --network tasks-net \
  -p 6379:6379 \
  redis:8-alpine
```

Проверка:

```bash
docker exec tasks-redis redis-cli ping   # -> PONG
```

## 4. Сборка образа приложения

```bash
cd /путь/к/Makedon-Docker
docker build -t tasks-app:local .
```

## 5. Запуск приложения

Хосты в URL — это имена контейнеров из шагов 2–3, а НЕ localhost. Внутри
контейнера `localhost` — это он сам, там никакого Postgres нет.

`CACHE_TTL_SECONDS=60` поставлен маленьким специально, чтобы в экспериментах
не ждать час.

```bash
docker run -d \
  --name tasks-app \
  --network tasks-net \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql+psycopg://postgres:admin@tasks-postgres:5432/postgres" \
  -e REDIS_URL="redis://tasks-redis:6379/0" \
  -e CACHE_TTL_SECONDS=60 \
  -e CORS_ALLOWED_ORIGINS="http://localhost:3000" \
  -e SQL_ECHO=0 \
  tasks-app:local
```

Логи в отдельном терминале — там будут строчки замеров:

```bash
docker logs -f tasks-app
```

Swagger: **http://127.0.0.1:8000/docs**

---

## 6. Проверяем, что кэш работает

В Swagger после каждого запроса смотри блок **Response headers**:

- `x-cache: MISS` — данные взяты из Postgres и только что положены в Redis
- `x-cache: HIT` — данные взяты из Redis
- `x-process-time-ms` — сколько заняла обработка всего запроса

Сценарий:

1. `POST /tasks` — создай 2–3 задачи.
2. `GET /tasks` → `x-cache: MISS`, время больше.
3. `GET /tasks` ещё раз → `x-cache: HIT`, время меньше.
4. `POST /tasks` (ещё одна) → кэш сброшен инвалидацией.
5. `GET /tasks` → снова `MISS`, и в списке есть новая задача.
6. Подожди больше 60 секунд, `GET /tasks` → `MISS` (TTL истёк сам).

Загляни в сам Redis:

```bash
docker exec -it tasks-redis redis-cli
> KEYS *
> TTL cache:tasks_list
> GET cache:tasks_list
```

## 7. Чтобы разница во времени стала очевидной

На 3 задачах разница между Postgres и Redis — единицы миллисекунд, её легко
принять за шум. Залей много строк:

```bash
docker exec -it tasks-postgres psql -U postgres -d postgres -c \
"INSERT INTO tasks (id, title, completed)
 SELECT gen_random_uuid()::text, 'task ' || g, false
 FROM generate_series(1, 50000) g;"
```

Сбрось кэш руками и замерь:

```bash
docker exec tasks-redis redis-cli DEL cache:tasks_list
```

Теперь `GET /tasks`: MISS будет заметно дороже HIT.

> Кстати, это сразу показывает главную боль кэширования: мы вставили строки
> напрямую в БД, минуя приложение, — и приложение об этом не узнало. Пока ты не
> сделал `DEL` вручную, API продолжал отдавать старый список из Redis. Любая
> запись в обход сервиса = протухший кэш.

Замер «снаружи», без Swagger:

```bash
curl -s -o /dev/null -D - http://127.0.0.1:8000/tasks | grep -i -E "x-cache|x-process-time"
```

## 8. Остановить и убрать

```bash
docker rm -f tasks-app tasks-redis tasks-postgres
docker network rm tasks-net
docker volume rm tasks_pg_data   # только если нужно снести данные
```
