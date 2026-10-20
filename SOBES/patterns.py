'''
Unit of Work (UoW) — это паттерн, который отслеживает изменения объектов в рамках одной бизнес-транзакции
и в конце применяет их все разом (одним commit), либо откатывает всё целиком при ошибке.

Главная идея: вместо того чтобы сохранять каждое изменение в БД по отдельности
(создал — сразу insert, изменил — сразу update), ты накапливаешь все изменения в памяти,
а потом фиксируешь их одной атомарной операцией.

Зачем это нужно:

Консистентность — если одна из операций в транзакции упадёт, откатываются все, а не часть
Производительность — можно сгруппировать запросы (batch insert/update) вместо кучи отдельных обращений к БД
Разделение ответственности — бизнес-логика не думает про commit/rollback на каждом шаге, этим занимается UoW

'''

import sqlite3

class UnitOfWork:
    def __init__(self, db_path):
        self.db_path = db_path

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()   # всё прошло успешно — фиксируем
        else:
            self.connection.rollback() # была ошибка — откатываем всё
        self.connection.close()

    def execute(self, query, params=()):
        self.connection.execute(query, params)


# использование
with UnitOfWork("app.db") as uow:
    uow.execute("INSERT INTO users (name) VALUES (?)", ("Den",))
    uow.execute("UPDATE accounts SET balance = balance - 100 WHERE user_id = 1")
    # если здесь вылетит исключение — обе операции откатятся




'''
На практике — SQLAlchemy
В реальных Python-проектах UoW почти всегда встроен в SQLAlchemy Session — она сама отслеживает изменённые объекты 
и копит их до commit():
'''


'''
from sqlalchemy.orm import Session

with Session(engine) as session:
    user = session.get(User, 1)
    user.name = "New Name"          # изменение просто запомнено в памяти

    new_order = Order(user_id=1, total=99.9)
    session.add(new_order)          # тоже пока не в БД

    session.commit()                # вот тут ВСЁ applies одним махом (UPDATE + INSERT)
'''




'''в связке с repository'''
'''
class SqlAlchemyUnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)  # репозитории живут внутри UoW
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


# использование в бизнес-логике
def transfer_money(uow, from_id, to_id, amount):
    with uow:
        sender = uow.users.get(from_id)
        receiver = uow.users.get(to_id)
        sender.balance -= amount
        receiver.balance += amount
        uow.commit()  # обе операции фиксируются вместе
'''




