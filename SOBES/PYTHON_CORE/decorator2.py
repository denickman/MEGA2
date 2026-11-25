

import functools
from functools import wraps
from time import perf_counter, sleep
from typing import Callable

from inspect import iscoroutinefunction


def print_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Begin func...")
        result = func(*args, **kwargs)
        print("End func...")
        return result
    return wrapper


@print_decorator
def simple_print():
    ''' super mega method ever made '''
    print("do soemthing useful")

simple_print()

# same shit
# simple = print_decorator(simple_print)
# simple()

print("======================")
print(f"Name of func: {simple_print.__name__}" )
print(f"Doca: {simple_print.__doc__}")








@print_decorator
def create_user(email: str, name: str):
    user = {
        'email': email,
        'name': name
    }
    print("CREATE USER")
    return user

print("---------------------------------")
print("Start time")
start = perf_counter()
sleep(2.0)
end = perf_counter()
print("End time")

print(f'Delta time: {end - start}')








def decora(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"Delta time: {end - start}")
        return result
    return wrapper





# with params





def timer_limit(seconds: int):
    """
       Декоратор-фабрика: ограничивает время выполнения функции.
       Если функция выполняется дольше `seconds` секунд — бросает TimeoutError.
       """
    def decorator_timer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = perf_counter()
            result = func(*args, **kwargs)
            end = perf_counter() - start

            print(f'Function {func.__name__} time: {end} seconds')

            if end > seconds:
                raise TimeoutError(
                    f'Function {func.__name__} exceeded limit: '
                    f'{end:.4f}s > {seconds}s'
                )
            return result
        return wrapper
    return decorator_timer


@timer_limit(1)
def get_something():
    return 123



@timer_limit(1)
def slow_something():
    sleep(2)
    return 456



try:
    slow_something()
except TimeoutError as e:
    print(f"error {e}")







def sync_func():
    ...

async def async_func():
    ...

print(iscoroutinefunction(sync_func))
print(iscoroutinefunction(async_func))








from functools import wraps
from inspect import iscoroutinefunction
from time import perf_counter


def timer_limit_universal(seconds: float):
    def decorator_timer(func):

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = perf_counter()
            result = func(*args, **kwargs)
            elapsed = perf_counter() - start
            print(f'[sync] {func.__name__}: {elapsed:.4f}s')
            if elapsed > seconds:
                raise TimeoutError(f'{func.__name__} exceeded {seconds}s')
            return result

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = perf_counter()
            result = await func(*args, **kwargs)
            elapsed = perf_counter() - start
            print(f'[async] {func.__name__}: {elapsed:.4f}s')
            if elapsed > seconds:
                raise TimeoutError(f'{func.__name__} exceeded {seconds}s')
            return result

        return async_wrapper if iscoroutinefunction(func) else sync_wrapper

    return decorator_timer



@timer_limit(1)
def sync_func():
    return 'sync result'

@timer_limit(1)
async def async_func():
    return 'async result'


