from socket import create_connection




print("################# asyncio ################")

import asyncio

async def task(name, delay):
    print(f"{name} start")
    await asyncio.sleep(delay)
    print(f"{name} end")

async def main():
    await asyncio.gather(
        task("A", 2),
        task("B", 3),
    )

asyncio.run(main())





























print("################# GIL ################")
# global interpreter lock
# это блокировка внутри CPython (стандартной реализации Python), которая разрешает только одному потоку выполнять
# Python-байткод в любой момент времени, даже если у тебя несколько потоков и многоядерный процессор.













print("################# error handling ################")

user_input = input('Enter some: ')

try:
    value = int(user_input)
    result = 100/value
except ZeroDivisionError:
    print("Нельзя делить на ноль")
except ValueError:
    print('enter a number')
except Exception as e:
    print('something went wrong dude:', e)  # покажет реальную причину
else:
    print(f'result it {result}')
finally:
    print('FINALLY always called')



print("################# custom error ################")
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        # У Exception есть свой __init__, который сохраняет переданный текст в специальный атрибут args, и благодаря этому работает str(e) и print(e):
        super().__init__(f"Cannot withdraw {amount}, balance is {balance}")


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


try:
    new_balance = withdraw(100, 150)
except InsufficientFundsError as e:
    print(e)                # Cannot withdraw 150, balance is 100
    print(e.balance)        # 100
    print(e.amount)         # 150
else:
    print(f"Новый баланс: {new_balance}")





print("################# INITIAL ################")




def add_item(item: str, items =[]):
    items.append(item)
    return items

add_item('apple')
lastone = add_item('banana')

for i in lastone:
    print(i)


def add_item_correct(item: str, items:list[str] = None):
    if items is None:
        items = []

    items.append(item)
    return items

items = add_item_correct('apple')
items2 = add_item_correct('newone')

print(items)
print(items2)






a = [1,2]
b = [1,2]

c = a

print(a == b)
print(a is b)
print(a is c)




# генератор одноразовый
# generator func
def count_up_to(n: int):
    i = 1
    while i <= n:
        yield i
        i += 1

generator = count_up_to(10)

print(next(generator))
print(next(generator))




# print(generator)
#
# for element in generator:
#     print(element)

# generator выражение
squares = (x**2 for x in range(10))
print(squares)
print(list(squares))

# Зачем нужны
#
# Главный плюс — экономия памяти. Если тебе нужно обработать миллион элементов, список хранит все миллион в памяти,
# а генератор хранит только текущее состояние (где он остановился) и выдаёт по одному.


# list
squares_list = [x**2 for x in range(5)]  # вычисляется ВЕСЬ список сразу










def gen():
    i = 0
    while True:
        received = yield i
        if received == "stop":
            return
        i += 1


g = gen()
print(next(g))        # 0 — запускает генератор до первого yield
# print(g.send(None))   # 1 — "посылает" значение внутрь, оно становится результатом yield
# print(g.send("stop"))  # StopIteration — завершили через return
# g.throw(ExceptionType)
# g.close()


# yield from — делегирование другому генератору/итерируемому
def inner():
    yield 1
    yield 2

def outer():
    yield 0
    yield from inner()   # разворачивает все значения inner()
    yield 3

print(list(outer()))  # [0, 1, 2, 3] сам прогоняет next



print("#################decorator################")

import functools
import time


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f'{func.__name__} took {elapsed:.3f} seconds')
        return result
    return wrapper

@timer
def process_data(n):
    """process n items"""
    result = sum(range(n))
    print(f'{n} items processed: {result}')
    return result

process_data(5)




print("################# context manager class ################")


# with open('data.text', 'r') as f:
#     data = f.read()

# custom context manger
# using class approach

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start
        if exc_type is not None:
            print(f"упало с {exc_type.__name__} после {elapsed:.3f}s")
        if exc_type is ZeroDivisionError:
            print("деление на ноль проигнорировано")
            return True  # только эту одну ошибку осознанно гасим
        else:
            print(f"elapsed: {elapsed:.3f}s")
        return False  # исключение полетит дальше наверх

# with Timer() as t:
#     sum(range(10_000_000))
#     raise ValueError("что-то не так")

print("################# contextmanager ################")


# using @contextmanager
from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f'elapsed time: {elapsed:.3f} seconds')


with timer():
    sum(range(10_000_000))



@contextmanager
def open_file(path):
    f = open(path)
    try:
        yield f
    finally:
        f.close()

with open_file('test.txt') as f:
    print(f.read())



