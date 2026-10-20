"""
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

"""

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
