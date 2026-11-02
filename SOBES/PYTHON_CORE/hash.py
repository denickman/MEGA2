

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y)) # хеш из тех же полей, что и __eq__


p1, p2 = Point(1, 2), Point(1, 2)
print(p1 == p2)  # True
print({p1, p2})  # один элемент — set их схлопнул

'''
Ловушка: если определить только__eq__и не определить __hash__
Python выставит __hash__ = None и объект станет нехешируемым. Это защита от
нарушения контракта. То же самое делает @dataclass(eq=True) — поэтому для
dataclass, который нужно класть в set, пишут @dataclass(frozen=True): он
генерирует и __eq__, и__hash__
'''




from dataclasses import dataclass

@dataclass
class Point:          # eq=True по умолчанию
    x: int
    y: int
# __hash__ = None → нельзя класть в set/dict

@dataclass(frozen=True)
class Point:
    x: int
    y: int
# генерируются и __eq__, и __hash__ → можно класть в set/dict