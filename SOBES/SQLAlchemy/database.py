from sqlalchemy import create_engine, text
from config import settings
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase


# sync
sync_engine = create_engine(
    url=settings.DATABASE_URL_sqlite,
    echo=True,
)

# async
# async_engine = create_engine(
#     url=settings.DATABASE_URL_asyncpg,
#     echo=True,
# )



# begin - если хочешь чтобы при выходе из контекстного менеджена делался коммит
# connect - если не хочешь и явно прописываешь коммит если тебе это надо

with sync_engine.connect() as conn:
    res = conn.execute(text('SELECT sqlite_version()'))
   # res = conn.execute(text('SELECT 1,2,3 union select 4,5,6'))


    print(f"1.{res.all()=}")
    print(f"2.{res.first()=}")
    # print(res.fetchone())



session_factory = sessionmaker(bind=sync_engine)
# async_session_factory = sessionmaker(bind=sync_engine)




'''
DeclarativeBase — это специальный базовый класс из SQLAlchemy, который подключает декларативную ORM-систему: механизм, 
который превращает обычный Python-класс в класс, привязанный к таблице БД.

Когда WorkerOrm наследуется от Base (а значит транзитивно от DeclarativeBase), при создании класса срабатывает 
специальная "магия" (метаклассы/__init_subclass__) внутри DeclarativeBase, которая:

Сканирует атрибуты класса (id: Mapped[int] = mapped_column(...)) и превращает их в описание колонок таблицы.
Регистрирует класс в общем реестре — все классы, унаследованные от одного Base, автоматически попадают в 
единый Base.metadata (тот самый MetaData, который потом используется в Base.metadata.create_all()).
Даёт классу ORM-поведение — именно благодаря этому WorkerOrm(username='bobr') создаёт обычный Python-объект, 
а Session потом умеет его отслеживать, сравнивать с БД, генерировать INSERT/UPDATE и т.д.

Зачем нужен именно свой Base, а не DeclarativeBase напрямую

Технически можно было бы писать class WorkerOrm(DeclarativeBase) напрямую, но тогда у каждого класса был бы свой 
собственный metadata-реестр — и create_all() создавал бы только одну таблицу за раз.

Создавая один общий Base (твой class Base(DeclarativeBase): pass) и наследуя от него все модели (WorkerOrm, и 
любые другие будущие классы), ты объединяешь их все в один общий Base.metadata — поэтому 
Base.metadata.create_all(sync_engine) создаст сразу все таблицы всех классов, унаследованных от этого Base, 
одной командой — ровно та же идея, что и с metadata_object в Core-подходе, просто для ORM-классов.

Короче: DeclarativeBase — это "включатель" ORM-механики на класс, а твой собственный Base — это общая точка сборки, 
чтобы все модели жили в одном реестре метаданных.
'''

class Base(DeclarativeBase):
    pass



