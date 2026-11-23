# Это прямой аналог Swift-протоколов, появился в Python 3.8 (typing.Protocol):
from typing import TypeVar
from typing import Protocol

class Comparable(Protocol):
    def __lt__(self, other) -> bool: ...

T = TypeVar("T", bound=Comparable)

def smallest(items: list[T]) -> T:
    return min(items)





'''
Это structural typing (аналог duck typing, но с проверкой типов) — объект подходит под Protocol, 
если у него есть нужные методы/атрибуты, даже без явного наследования от этого протокола 
(в отличие от обычных абстрактных классов, где нужно explicit class MyClass(Comparable):).
'''