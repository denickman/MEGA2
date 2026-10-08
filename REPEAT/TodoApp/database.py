# database.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

"""
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
"""


# for local db
# SQLALCHEMY_DATABASE_URI = 'sqlite:///./todosapp.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})


# need install pip install "psycopg[binary]"
# for postgresql
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwerty123!@localhost/TodoAppDatabase'
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)




SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]



"""
1. Swagger. Это страница /docs, которую FastAPI генерирует сам. Когда вы жмёте Execute, браузер отправляет обычный HTTP-запрос (его видно в блоке Curl на вашем скриншоте).

2. FastAPI. Запрос попадает в ваш обработчик Create User. Pydantic проверяет JSON, затем код обычно создаёт объект модели Users(...). Пароль при этом хешируется: в базе лежит $2b$12$..., это bcrypt, а не qwerty123. Ответ null со статусом 201 значит, что функция ничего не вернула (return нет), но создание прошло.

3. get_db и db_dependency. Для каждого запроса Depends(get_db) открывает новую сессию (SessionLocal()), отдаёт её в обработчик, а после ответа закрывает (finally: db.close()). Сессия это «рабочая область» с объектами, которые вы добавили, но ещё не записали.

4. db.add(obj) и db.commit(). add только помечает объект. На commit SQLAlchemy формирует SQL-запрос INSERT INTO users (email, username, ..., hashed_password) VALUES (...) и отправляет его в базу. Без commit данные не сохранятся.

5. engine. Это объект, который знает, куда и как подключаться (по строке SQLALCHEMY_DATABASE_URI) и держит пул соединений. Строка читается так:

postgresql://  postgres  :  qwerty123!  @  localhost  /  TodoAppDatabase
   драйвер      логин        пароль       хост         имя базы

6. Таблицы. Классы в models.py наследуются от Base. Таблицы создаёт обычно Base.metadata.create_all(bind=engine) в main.py, поэтому users и todos сами появились в базе.

pgAdmin на вашем скриншоте не участвует в процессе. Это просто ещё один клиент, который подключается к той же базе и делает select * from users. Поэтому вы видите там ту же строку, что создали через Swagger.

Где находится сервер

Слово «сервер» здесь означает не «другой компьютер», а отдельный процесс, который слушает порт.

SQLite это библиотека внутри вашего Python-процесса. Она сама читает и пишет файл .db, ничего больше не запущено.
PostgreSQL это отдельная программа (процесс postgres), которая всегда работает в фоне и слушает порт 5432. Ваше приложение и pgAdmin подключаются к нему по сети, как к веб-серверу.

У вас в строке подключения localhost, то есть сервер Postgres запущен на вашем же Mac. Данные лежат в папке данных Postgres на вашем диске. Точный путь можно узнать запросом:

sql
SHOW data_directory;

Если ставили через Homebrew, это обычно что-то вроде /opt/homebrew/var/postgresql@17, у Postgres.app в ~/Library/Application Support/Postgres/. Руками в этих файлах копаться не нужно, ими управляет только Postgres.

Когда вы выложите приложение в продакшен, в строке поменяется только хост: вместо localhost будет адрес удалённого сервера с Postgres (например, облачная база). Код приложения останется тем же.

Servers в pgAdmin. ToDoAppServer2 и TodoAppServer3 это не серверы, а сохранённые подключения в pgAdmin. Значок с крестиком означает, что подключения сейчас нет.

"""