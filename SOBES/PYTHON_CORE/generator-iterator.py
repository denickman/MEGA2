

'''
Итератор vs Генератор — это НЕ одно и то же, генератор — частный случай итератора

list сам по себе не умеет "запоминать позицию" и отдавать элементы по одному — а итератор умеет.
Поэтому iter() оборачивает список в такой объект.

Итератор (Iterator) — любой объект, у которого есть метод __next__() (и __iter__(), возвращающий самого себя). Это общий протокол.

Генератор (Generator) — это один конкретный способ создать итератор — через функцию с yield.
Генератор автоматически реализует протокол итератора "под капотом", тебе не нужно вручную писать __next__/__iter__.



# Генератор — создаётся через yield, итератор получается "бесплатно"
def my_gen():
    yield 1
    yield 2



# Итератор, написанный руками — без yield, через явную реализацию протокола
class MyIterator:
    def __init__(self):
        self.values = [1, 2]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.values):
            raise StopIteration
        value = self.values[self.index]
        self.index += 1
        return value






Итератор — это объект, который умеет отдавать элементы по одному, через next().
Когда элементы кончаются — выбрасывает StopIteration.

numbers = [1, 2, 3]
it = iter(numbers)  # получили итератор

print(next(it))  # 1
print(next(it))  # 2
print(next(it))  # 3
print(next(it))  # StopIteration (ошибка — элементы кончились)


Чтобы сделать свой итератор, нужен класс с методами __iter__ и __next__:

class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        self.current += 1
        return self.current

for num in Counter(3):
    print(num)  # 1 2 3



Генератор — это упрощённый способ создать итератор, но вместо класса пишешь обычную функцию с ключевым словом yield.

def counter(limit):
current = 1
while current <= limit:
    yield current
    current += 1

for num in counter(3):
    print(num)  # 1 2 3


Главный плюс — экономия памяти. Генератор не хранит все значения сразу, а выдаёт их по требованию ("лениво").

# Плохо для больших чисел — весь список сразу в памяти
squares_list = [x**2 for x in range(1_000_000)]

# Хорошо — ничего не хранится, значения считаются по одному
squares_gen = (x**2 for x in range(1_000_000))


'''














# Generator[YieldType, SendType, ReturnType] — что такое 2-й и 3-й параметры

# YieldType — ты уже понял, это тип того, что генератор отдаёт через yield.

# SendType — тип значения, которое ты можешь передать ВНУТРЬ генератора через метод .send(value). Генератор —
# это не только "отдаёт наружу", он может и принимать данные обратно:

# ReturnType — тип значения, которое генератор возвращает через return (не yield, а именно return), когда полностью завершается:

# Это редко используется на практике (обычно работают только с yield "наружу"), поэтому в 99% случаев там пишут None —
# "генератор ничего не принимает через send".

from typing import Generator


def echo_gen():
    while True:
        received = yield "жду число"  # yield тут и отдаёт, и получает
        print(f"получил: {received}")

g = echo_gen()

print(next(g))      # "жду число"   — запустили генератор, дошли до первого yield
print(g.send(42))   # сначала выведет "получил: 42" (print внутри генератора),
                     # потом вернёт следующее "жду число" (от следующего прохода цикла)





def counter() -> Generator[int, None, str]:
    yield 1
    yield 2
    return "готово!"   # вот это ReturnType = str

g = counter()
next(g)   # 1
next(g)   # 2
next(g)   # StopIteration: готово!  <- возвращённое значение попадает в исключение StopIteration






'''
На практике, если генератор просто бесконечно отдаёт значения (как наш inf_gen) и никогда явно 
не return-ит что-то осмысленное — пишут None, None для обоих — "не принимает ничего, не возвращает ничего особенного".

from typing import Iterable, Generator, TypeVar
T = TypeVar("T")

def inf_gen(items: Iterable[T]) -> Generator[T, None, None]:
    # list(generator) работает — забирает ВСЕ элементы генератора в реальный список
    items = list(items)
    while items:
        for i in items:
            yield i

'''




