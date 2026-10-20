

'''

Да, можно. Python позволяет сделать декоратор через класс двумя разными способами — класс как сам декоратор,
или класс с методом __call__, который оборачивает функцию. Разберу оба, с примерами близкими к твоему FastAPI-коду.

Способ 1: класс-декоратор без аргументов

Класс может быть декоратором, если у него определён метод __call__ — тогда экземпляр класса
ведёт себя как вызываемый объект (callable), то есть его можно "вызвать" скобками, как функцию.


Разворачивая, что здесь произошло: @LogCalls — это то же самое, что say_hello = LogCalls(say_hello).
 Конструктор __init__ принял функцию и сохранил её, а когда ты вызываешь say_hello(), на самом деле
 вызывается __call__ у экземпляра класса LogCalls.
'''


class LogCalls:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f"Вызывается {self.func.__name__}")
        result = self.func(*args, **kwargs)
        print(f"{self.func.__name__} завершилась")
        return result


@LogCalls
def say_hello():
    print("hello")

say_hello()
# Вызывается say_hello
# hello
# say_hello завершилась








'''
Способ 2: класс-фабрика декоратора (с аргументами) — ближе к твоему FastAPI-случаю

Вспомни, @router.post("", response_model=...) — это фабрика, то есть вызов с аргументами, 
который возвращает декоратор. То же самое можно сделать через класс:

Разворачивая: @RateLimiter(max_calls=5) сначала создаёт экземпляр RateLimiter(max_calls=5) — вызывается __init__, 
параметр сохраняется. Затем этот экземпляр применяется к create_post как декоратор — вызывается __call__(create_post), 
который возвращает wrapper. В итоге create_post на самом деле становится wrapper.
'''

class RateLimiter:
    def __init__(self, max_calls):
        self.max_calls = max_calls   # параметры декоратора

    def __call__(self, func):
        # этот метод получает саму декорируемую функцию
        call_count = {"count": 0}

        async def wrapper(*args, **kwargs):
            call_count["count"] += 1
            if call_count["count"] > self.max_calls:
                raise Exception("Превышен лимит вызовов")
            return await func(*args, **kwargs)

        return wrapper


@RateLimiter(max_calls=5)
async def create_post(post, db):
    ...


'''
Когда класс-декоратор реально имеет смысл (а не просто "потому что можно")

Главное практическое преимущество класса — ему проще хранить состояние между вызовами, если это состояние сложное,
и удобнее добавлять дополнительные методы.
'''

class CallCounter:
    def __init__(self, func):
        self.func = func
        self.count = 0   # состояние хранится как атрибут класса, а не в замыкании

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

    def reset(self):          # дополнительный метод — такое неудобно делать через функцию
        self.count = 0


@CallCounter
def process():
    print("работаю")

process()
process()
print(process.count)   # 2 — можно напрямую читать состояние как атрибут объекта
process.reset()          # и вызывать методы на самом декораторе
print(process.count)   # 0









# fun tools
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("до")
        result = func(*args, **kwargs)
        print("после")
        return result
    return wrapper

@my_decorator
def hello():
    """Говорит привет"""
    print("привет")

# Проблема: после декорирования метаданные функции портятся.

print(hello.__name__)   # "wrapper" — а должно быть "hello"! __name__ — хранит имя функции как строку
print(hello.__doc__)     # None — а должно быть "Говорит привет" __doc__ — хранит docstring (строку документации) функции


# Это потому что hello теперь физически — это wrapper, а не оригинальная функция. functools.wraps чинит это:

from functools import wraps

def my_decorator(func):
    @wraps(func)             # вот это — ключевая строка
    def wrapper(*args, **kwargs):
        print("до")
        result = func(*args, **kwargs)
        print("после")
        return result
    return wrapper

@my_decorator
def hello():
    """Говорит привет"""
    print("привет")

print(hello.__name__)   # "hello" — исправлено
print(hello.__doc__)     # "Говорит привет" — исправлено





"""
Главное отличие от обычного декоратора — wrapper тоже должен быть async def, и вызов функции внутри — через await.
"""

import time
from functools import wraps
import asyncio

def async_timer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)   # важно: await, а не просто вызов
        end = time.time()
        print(f"{func.__name__} выполнилась за {end - start:.2f} сек")
        return result
    return wrapper


@async_timer
async def fetch_data():
    await asyncio.sleep(2)   # имитация долгого запроса
    return "данные получены"




