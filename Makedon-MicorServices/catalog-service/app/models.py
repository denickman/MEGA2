from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for ORM models.

    Base — это заготовка, шаблон. У неё нет __tablename__, то есть SQLAlchemy не знает, в какую таблицу её класть.
    Сама по себе она в Postgres ничего не создаёт.

    """

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )


class Product(Base):
    __tablename__ = "products"

    '''
        Product — это класс, который наследуется от Base (class Product(Base):), 
        то есть забирает себе всё, что в Base описано (поле id), и добавляет своё: __tablename__ = "products"
        и остальные колонки. Вот именно у Product уже есть всё необходимое, чтобы стать настоящей таблицей — имя и колонки.
    '''
    
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    image: Mapped[str]
    category: Mapped[str]

