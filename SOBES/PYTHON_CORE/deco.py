from functools import wraps


print('----functools.wraps-----')
# functools.wraps - Decorators



def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("До вызова")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def hello():
    """Это документация"""
    print("Привет")

print(hello.__name__)   # wrapper   ← плохо
print(hello.__doc__)    # None      ← плохо

print('----my deco-----')
def my_deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("---Before call----")
        return func(*args, **kwargs)
    return wrapper

@my_deco
def hello_nigga():
    'this is docss for the hello nigga function'
    print("kawabunga")

print(f'NAME: {hello_nigga.__name__}')
print(f'DOC: {hello_nigga.__doc__}')



print('----base deco-----')
def base_deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
            print('before call')
            result = func(*args, **kwargs)
            print('after call')
            return result
    return wrapper

@base_deco
def say_hello(name: str):
    'watafaka mazafaka'
    print(f'hello, {name}!')

say_hello('Koshake')


print('-----logger------')

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Вызываем {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def hello(name: str):
    print(f'hello, {name}')

hello('alexander')