


def get_first_matching_object(predicate, objects=[]):
    matching_objects = (obj for obj in objects if predicate(obj))

    if matching_objects:
        object = matching_objects[0]
        return object
    else:
        return None


'''
1. Главный баг: matching_objects — это генератор (generator expression в скобках), а не список. 
Проверка if matching_objects: всегда истинна, потому что сам объект-генератор всегда truthy, 
независимо от того, есть ли в нём элементы или нет. А строка matching_objects[0] вообще упадёт с 
TypeError: generator object is not subscriptable, т.к. генераторы не поддерживают индексацию.

2. Антипаттерн: objects=[] — изменяемый аргумент по умолчанию. В Python такой список создаётся 
один раз при определении функции и переиспользуется между вызовами — если его где-то случайно мутируют, 
это аукнется в следующих вызовах.

3. object — это встроенный тип в Python (базовый класс для всех объектов, object(), 
isinstance(x, object) и т.д.). Если назвать переменную object, она временно "затенит" (shadow)
встроенное имя в текущей области видимости — и пока переменная существует, обратиться к настоящему
object через это имя уже нельзя.
'''


def get_first_matching_object(predicate, objects=None):
    if objects is None:
        objects = []
    return next((obj for obj in objects if predicate(obj)), None)



def get_first_matching_object(predicate, objects=None):
    if objects is None:
        objects = []
    for obj in objects:
        if predicate(obj):
            return obj
    return None






# ====== decorator ======

import functools

def handle_exeptions(exception_callback):
    """
      exception_callbacks: список кортежей (exception_type, callback)
      callback вызывается как callback(exception) при совпадении типа исключения
      """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                for exc_type, callback in exception_callback:
                    if isinstance(exc, exc_type):
                        return callback(exc)
                raise  # ни один из указанных типов не подошёл — пробрасываем дальше
            return wrapper
        return decorator



print("=====================================================")
import threading
import time

counter = 0


def increment():
    global counter
    for _ in range(10):
        current = counter
        counter = current + 1

thread1 = threading.Thread(target=increment)
thread2 = threading.Thread(target=increment)

# После двух start() в процессе три потока:
# MainThread   → идёт по твоему коду: start, start, join, join, print
# Thread-1     → выполняет increment()
# Thread-2     → выполняет increment()

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(counter)




print("=====================================================")



import asyncio

async def say_hello():
    print('one')
    await asyncio.sleep(1)
    print('two')


async def main():
    await say_hello()
    task = asyncio.create_task(say_hello())
    print('three')
    await task

asyncio.run(main())

'''
Как это выглядит на твоём примере
 
asyncio.run(main()) создаёт event loop и кладёт в него main() как первую задачу.
Цикл запускает main(). Она идёт до своего await.
На await корутина уступает управление циклу.
Цикл смотрит в свою очередь, берёт следующую готовую задачу (например, say_hello), выполняет её до её await, и так по кругу.
Когда sleep(1) истёк, цикл помечает соответствующую задачу готовой и возвращается к ней.
Когда main() завершилась, цикл останавливается, и asyncio.run возвращает управление.
'''











'''


from dataclasses import dataclass, field

class Parent:
    def method(self) -> int:
        return 1

@dataclass(slots=True)
class Child[T: int](Parent):
    x: T
    y: list[int] = field(default=[])

    def method(self) -> str:
        return self.x + len(self.y) + super().method()

inst = Child[Any](y=1, x=5.5)
print(inst.method())


Проблема 1:

# Падает сразу при объявлении класса (field(default=[]) запрещён для изменяемых значений). 
field(default=[]) — это ошибка в принципе для dataclass. Изменяемые объекты (list, dict, set) нельзя давать через default=, 
потому что все экземпляры разделяли бы один и тот же список (классическая ловушка "mutable default argument", 
только для dataclass она ловится явно с ошибкой на этапе объявления класса)

Проблема 2: y=1 вместо списка

При создании объекта Child[Any](y=1, x=5.5) поле y объявлено как list[int], но ему передают 1 (int). 
В самой строке создания ошибки нет — Python рантайм не проверяет типы аннотаций, но внутри method() вызывается len(self.y), 
а у int нет len():

TypeError: object of type 'int' has no len()


Проблема 3: x=5.5 нарушает bound дженерика
class Child[T: int] — это PEP 695 generic с ограничением T: int, то есть T должен быть int (или его подтипом). 
Но передают x=5.5 (float). Рантайм это не остановит (аннотации типов — это для статических чекеров типа mypy/pyright, 
не для исполнения), но намерение кода явно нарушено: вызов противоречит собственной сигнатуре класса. 
Статический type-checker эту строку бы отклонил.

Похоже, x и y просто перепутаны местами при вызове — явно должно быть x=1, y=[...] или что-то в этом духе.

Проблема 4 (менее критично, но стоит знать): super() + slots=True

slots=True на dataclass в целом нормально сочетается с super(), но будь аккуратен, 
если Parent — не dataclass и не имеет __slots__ сам: тогда у Child всё равно будет __dict__ от родителя, 
и часть экономии памяти от slots=True потеряется. Это не ошибка, но частое заблуждение "раз указал slots=True, 
значит объект точно без __dict__".


'''


# better

'''
field(default=[]) → field(default_factory=list) — чтобы экземпляры не делили один и тот же список.
x=5.5 → x=5 и Child[Any] → Child[int] — T ограничен int (T: int), а дробное число нарушало это ограничение.
Местами перепутанные x и y в вызове конструктора поменял на правильные (x — число, y — список).
-> str → -> int в сигнатуре method — возвращаемое значение на деле целое число, аннотация была неверной.
Добавил from typing import Any — в исходнике Any использовался без импорта, что само по себе NameError.
'''

from dataclasses import dataclass, field
from typing import Any

class Parent:
    def method(self) -> int:
        return 1

@dataclass(slots=True)
class Child[T: int](Parent):
    x: T
    y: list[int] = field(default_factory=list)

    def method(self) -> int:
        return self.x + len(self.y) + super().method()

inst = Child[int](x=5, y=[1, 2, 3])
print(inst.method())   # 9








'''
-- authors

-- author_id | name
-- ----------+-------------------
-- 1         | Александр Пушкин
-- 2         | Лев Толстой
-- 3         | Федор Достоевский
-- 4         | Антон Чехов
-- 5         | Михаил Булгаков


-- books

-- book_id | author_id | title
-- --------+-----------+---------------------------
-- 1       | 1         | Евгений Онегин
-- 2       | 1         | Капитанская дочка
-- 3       | 1         | Руслан и Людмила
-- 4       | 2         | Война и мир
-- 5       | 2         | Анна Каренина
-- 6       | 3         | Преступление и наказание
-- 7       | 3         | Братья Карамазовы
-- 8       | 4         | Вишневый сад
-- 9       | 5         | Мастер и Маргарита
-- 10      | 5         | Собачье сердце



просто имена без счетчика 
====
SELECT a.name
FROM authors a
JOIN books b ON b.author_id = a.author_id
GROUP BY a.author_id, a.name
HAVING COUNT(b.book_id) >= 2;


со счетчиком 
=====
SELECT a.author_id, a.name, COUNT(b.book_id) AS books_count
FROM authors a
JOIN books b ON b.author_id = a.author_id
GROUP BY a.author_id, a.name
HAVING COUNT(b.book_id) >= 2;

'''










