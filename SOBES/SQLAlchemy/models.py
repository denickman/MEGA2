from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from database import Base
from sqlalchemy.orm import Mapped, mapped_column


# declarative style
class WorkerOrm(Base):
    __tablename__ = 'workers_orm'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()


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
