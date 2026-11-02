import datetime
from turtledemo import forest

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, func, text
from database import Base, str_200
from sqlalchemy.orm import Mapped, mapped_column
import enum
from typing import Optional, Annotated


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                          onupdate=datetime.datetime.now)]



class WorkLoad(enum.Enum):
    parttime = 'parttime'
    fulltime = 'fulltime'




# declarative style
class WorkersOrm(Base):
    __tablename__ = 'workers'
    #id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[intpk]
    username: Mapped[str] # = mapped_column() you may not write mapped_column


class ResumesOrm(Base):
    __tablename__ = 'resumes'

    # id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[intpk]
    title: Mapped[str_200] # = mapped_column(String(50))
    compensation: Mapped[int | None]
    workload: Mapped[WorkLoad]
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete="CASCADE")) # 'SET NULL'
    # created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    # updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
    #                                                       onupdate=datetime.datetime.now)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

'''
server_default — значение по умолчанию задаётся на уровне базы данных. Оно прописывается прямо в DDL (CREATE TABLE), 
и БД сама подставляет его, если значение не передано в INSERT — даже если запись делается не через SQLAlchemy 
(сырым SQL, другим приложением, вручную в консоли БД).

python
created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

default — значение задаётся на уровне Python/SQLAlchemy, перед отправкой INSERT в базу. Если ты создашь объект без 
этого поля, SQLAlchemy сам вычислит значение в момент сохранения и добавит его в запрос. Но если кто-то вставит 
запись в обход SQLAlchemy (сырым SQL), это значение не подставится.

python
created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

Коротко: server_default — гарантия на уровне БД (надёжнее, работает всегда), default — гарантия на уровне приложения 
(работает только если вставка идёт через SQLAlchemy).
 '''






# imperative style
metadata_object = MetaData()
workers_table = Table(
    'workers',
    metadata_object,
    Column('worker_id', Integer, primary_key=True),
    Column('username', String),
)



'''
MetaData — это реестр, который хранит описания всех твоих таблиц (их структуру: колонки, типы, связи, индексы) в одном месте.

Зачем он нужен:

Группировка таблиц — все Table, созданные с одним metadata_object, становятся его частью, и SQLAlchemy знает о них как о едином наборе.
Создание/удаление схемы одной командой:

Без MetaData пришлось бы создавать каждую таблицу по отдельности.
3. Разрешение связей между таблицами — когда у тебя ForeignKey('workers.id'), SQLAlchemy ищет таблицу workers именно 
в этом объекте metadata_object, чтобы построить связь.

4. Интроспекция — можно считать существующую структуру БД в MetaData (metadata_object.reflect(engine)), не описывая таблицы руками.





Вот в чём принципиальная разница sessions:

Ты создаёшь обычные Python-объекты (WorkerOrm(username='bobr')) — это экземпляры твоего класса, 
с которыми можно работать как с любыми Python-объектами: передавать в функции, менять атрибуты, проверять условия 
и т.д. до того, как они попадут в БД.

Session — это не просто соединение, а "единица работы" (Unit of Work). Она:
отслеживает все объекты, которые ты в неё добавил (session.add),
сама строит нужные SQL-запросы (INSERT) при вызове commit() или flush() — тебе не нужно писать insert(...) вручную,
отслеживает изменения — если ты потом изменишь worker_bobr.username = 'new_name' и снова сделаешь commit(), 
Session сама поймёт, что нужен UPDATE, без твоего явного запроса,
кеширует объекты (Identity Map) — если дважды запросить один и тот же id, вернётся тот же Python-объект, а не новый.

conn.execute(statement); conn.commit() в Core-варианте — это разовое "выполни этот SQL и зафиксируй", без памяти о состоянии объектов.
session.add(obj); session.commit() в ORM-варианте — это "зарегистрируй изменение в этом объекте, 
а как собрать правильный SQL (INSERT/UPDATE/DELETE) — решу я сама при коммите".

Главная суть различия: Core — ты думаешь в терминах "таблицы и запросы" (ближе к SQL). ORM/Session — ты думаешь 
в терминах "объекты и их состояние" (ближе к обычному Python/ООП), а SQLAlchemy сам транслирует изменения объектов в SQL за кулисами.

Это тот же принцип, что ORM вообще — абстрагирует тебя от SQL, давая работать с данными как с обычными 
классами/объектами языка, что обычно удобнее в больших приложениях (например, хочешь добавить юзера, 
сохранить его в разных местах кода, модифицировать перед сохранением — с ORM это естественный Python-код, 
а не ручная сборка SQL-запросов).

'''
