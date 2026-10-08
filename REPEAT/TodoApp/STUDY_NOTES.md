# Учебные заметки — TodoApp

Этот файл для справки: здесь собраны все секреты, строки подключения
и полезные команды, чтобы было удобно находить при обучении.

---

## Секреты и строки подключения

### JWT Secret Key
```
SECRET_KEY = 8ef19e4387d76b6c2125f73c94f5e97688643893f69052ff0f8091bb6e272fab
ALGORITHM = HS256
```
Сгенерировать новый ключ: `openssl rand -hex 32`

### SQLite (локальная, файловая)
```
sqlite:///./todosapp.db
```
- Файл создаётся автоматически при первом запуске
- Аргумент `connect_args={"check_same_thread": False}` нужен только для SQLite

### PostgreSQL
```
postgresql://postgres:qwerty123!@localhost/TodoAppDatabase
```
Разбор строки подключения:
```
postgresql://  postgres  :  qwerty123!  @  localhost  /  TodoAppDatabase
   драйвер      логин        пароль       хост         имя базы
```
- Нужен драйвер: `pip install "psycopg[binary]"`
- `echo=True` в `create_engine` — печатает SQL-запросы в консоль (для отладки)

### MySQL
```
mysql+pymysql://root:password@localhost/TodoAppDatabase
```
- Драйвер: `pip install pymysql`

---

## Полезные команды

### Запуск приложения
```bash
uvicorn app.main:app --reload
```
После рефакторинга: `app.main:app` вместо `main:app`,
потому что `main.py` теперь внутри папки `app/`.

### Alembic (миграции)
```bash
# Инициализация (один раз)
alembic init alembic

# Создать миграцию вручную
alembic revision -m "описание миграции"

# Создать миграцию автоматически (по разнице моделей и БД)
alembic revision --autogenerate -m "описание миграции"

# Применить все миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1
```

### Виртуальное окружение
```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
pip install -r requirements.txt
```

### Зависимости проекта
```bash
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings
pip install python-jose[cryptography] passlib[bcrypt]
pip install "psycopg[binary]"   # только для PostgreSQL
pip install alembic
```

---

## Как работает поток данных

```
Swagger UI (браузер)
   │  HTTP POST /auth/auth + JSON
   ▼
FastAPI (uvicorn, :8000)
   │  валидация, хеширование пароля, db.add / db.commit
   ▼
SQLAlchemy (engine + session)
   │  превращает Python-объект в SQL: INSERT INTO users ...
   ▼
драйвер psycopg
   │  TCP-соединение на localhost:5432
   ▼
PostgreSQL → записывает на диск
```

---

## Структура проекта после рефакторинга

```
TodoApp/
├── .env                  # секреты (НЕ в git)
├── .env.example          # шаблон для .env
├── .gitignore
├── STUDY_NOTES.md        # этот файл
├── alembic.ini
├── alembic/              # миграции БД
│   ├── env.py
│   └── versions/
├── app/
│   ├── main.py           # точка входа FastAPI
│   ├── database.py       # engine, session, Base
│   ├── models.py         # ORM-модели (Users, Todos)
│   ├── core/
│   │   ├── config.py     # настройки из .env (pydantic-settings)
│   │   └── security.py   # bcrypt, JWT, OAuth2
│   ├── schemas/
│   │   ├── auth.py       # CreateUserRequest, Token
│   │   ├── todo.py       # TodoRequest
│   │   └── user.py       # UserVerification, UserResponse, PhoneNumberRequest
│   └── routers/
│       ├── auth.py       # регистрация, логин, токены
│       ├── todos.py      # CRUD для задач
│       ├── users.py      # профиль, смена пароля
│       └── admin.py      # админ-эндпоинты
```
