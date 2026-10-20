import sys

import sys

s = "hello world this is a longer string"
print(f'Ref count: {sys.getrefcount(s)}')   # покажет количество ссылок (обычно +1, т.к. сам getrefcount тоже временно ссылается)

# a = s
# print(sys.getrefcount(s))   # счётчик вырос — теперь ссылаются и s, и a
#
# del a
# print(sys.getrefcount(s))   # счётчик упал обратно


'''
Уровень 2: циклический сборщик мусора (cyclic garbage collector) — вот чего нет в чистом ARC

Reference counting ломается в одном конкретном случае — циклические ссылки, когда два объекта ссылаются друг на друга, 
и счётчик у обоих никогда не упадёт до нуля сам по себе, даже если снаружи на них уже никто не ссылается.
'''


class Node:
    def __init__(self):
        self.ref = None

a = Node()
b = Node()

a.ref = b   # a ссылается на b
b.ref = a   # b ссылается на a

del a
del b
# теперь ни одна внешняя переменная не указывает ни на a, ни на b,
# НО a.ref указывает на b, а b.ref указывает на a —
# счётчики ссылок у обоих объектов НЕ равны нулю, хотя до них уже не добраться