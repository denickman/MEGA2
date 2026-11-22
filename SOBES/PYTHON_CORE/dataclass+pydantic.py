"""

dataclass vs Pydantic — в чём разница

Обе штуки решают одну базовую задачу — не писать руками __init__, __repr__, __eq__
для класса, который просто хранит данные. Но дальше они расходятся сильно.



dataclass -
Это декоратор,
который автоматически генерирует часто нужные методы для классов, которые в основном просто хранят данные —
избавляет от написания шаблонного кода (__init__, __repr__, __eq__ и т.д.) вручную.


@dataclass из коробки генерирует только три самых часто нужных дандера для "класса-данных": __init__, __repr__, __eq__.
Остальные (__add__, __len__, __iter__, __call__ и т.д.) — это всё ещё твоя ответственность, как в обычном классе,
потому что это уже специфичное поведение, которое зависит от смысла твоего класса, а не от того, что он просто "хранит данные".


Это автоматически даёт тебе:

Метод	Что делает
__init__	Конструктор — Point(1, 2) работает сразу
__repr__	Красивый вывод — Point(x=1, y=2)
__eq__	Сравнение по значению полей — Point(1,2) == Point(1,2) → True


__add__, __len__, __lt__ (и другие сравнения типа <, >) — их @dataclass не генерирует автоматически, потому что непонятно,
что они должны значить для твоего конкретного класса. Складывать точки покоординатно? Или как-то иначе?
Python не может угадать твою бизнес-логику — поэтому такие методы ты всё ещё должен писать сам, как в обычном классе




@dataclass(frozen=True)      # неизменяемый + появляется __hash__
class Point:
    x: int
    y: int

@dataclass(order=True)       # можно сравнивать <, >, <=, >=
class Point:
    x: int
    y: int



"""


# dataclass (встроено в Python, from dataclasses import dataclass)

from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

u = User("Den", 30)
print(u)              # User(name='Den', age=30) — __repr__ сгенерирован
u2 = User("Den", 30)
print(u == u2)        # True — __eq__ сгенерирован


# Без @dataclass тебе бы пришлось писать это руками:
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __repr__(self): ...
    def __eq__(self, other): ...


# Важно: dataclass НЕ проверяет типы в runtime.
u = User("Den", "тридцать")   # никакой ошибки! age=str, а не int
print(u.age)   # "тридцать" — и никто не пожаловался

# Pydantic (сторонняя библиотека, pip install pydantic)
# Делает всё то же самое, плюс реально проверяет и валидирует данные в runtime, при создании объекта.

# Вот ключевая разница: Pydantic реально проверяет тип при создании объекта, и если данные не подходят —
# выбрасывает понятную ошибку с деталями (какое поле, что не так). А если можно безопасно преобразовать
# (строка "30" → int) — сделает это сам (coercion).

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

u = User(name="Den", age="30")   # строка "30" на входе!
print(u.age, type(u.age))        # 30 <class 'int'> — Pydantic САМ преобразовал строку в int!

u2 = User(name="Den", age="тридцать")
# ValidationError: age — value is not a valid integer



# Зачем это нужно
# Главный кейс использования — граница внешних данных: JSON из API-запроса, данные из конфига, тело HTTP-запроса.
# Там ты не контролируешь, что придёт — и нужна проверка "а это точно то, что я ожидаю?"



# пришёл JSON от клиента, тип данных неизвестен заранее
raw_data = {"name": "Рекс", "age": "5"}   # возраст как строка — так бывает из форм/JSON
user = User(**raw_data)   # Pydantic провалидирует и сконвертирует

'''
Именно поэтому Pydantic — основа FastAPI: там входящие запросы автоматически валидируются через Pydantic-модели, 
и если клиент прислал мусор — FastAPI сам вернёт 422 с описанием ошибки.

Дополнительные плюсы Pydantic
.model_dump() / .model_dump_json() — сериализация в dict/JSON "из коробки".
Вложенные модели, кастомные валидаторы (@field_validator), значения по умолчанию, алиасы полей.
Генерация JSON Schema (используется в автодокументации FastAPI — Swagger/OpenAPI).
'''

from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    age: int

    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("age должен быть положительным")
        return v








# Без dataclass — пишешь всё руками
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# С dataclass — то же самое в разы короче
# Декоратор @dataclass сам создаёт __init__, __repr__, __eq__ на основе объявленных полей с аннотациями типов.

from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p1 = Point(1, 2)
p2 = Point(1, 2)

print(p1)           # Point(x=1, y=2) — __repr__ сгенерирован автоматически
print(p1 == p2)      # True — __eq__ тоже сгенерирован автоматически




# Полезные параметры декоратора
from dataclasses import dataclass

@dataclass(frozen=True)  # делает объект неизменяемым (immutable), как tuple
class ImmutablePoint:
    x: int
    y: int

p = ImmutablePoint(1, 2)
# p.x = 5  # FrozenInstanceError — нельзя изменить после создания






@dataclass(order=True)  # добавляет __lt__, __le__, __gt__, __ge__ — можно сравнивать (<, >, и т.д.)
class Version:
    major: int
    minor: int

v1 = Version(1, 2)
v2 = Version(1, 5)
print(v1 < v2)  # True



@dataclass
class Rectangle:
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height

r = Rectangle(3, 4)
print(r.area())  # 12
