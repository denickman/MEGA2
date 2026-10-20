
'''
Декоратор — это функция, которая принимает другую функцию и возвращает (обычно) новую функцию, обёрнутую вокруг исходной.
'''

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("--BEFORe--")
        result = func(*args, **kwargs)
        print('--AFTER--')
        return result
    return wrapper


@my_decorator
def say_hello():
    print("Hello World")


say_hello()


'''
# простой декоратор — применяется сразу
@my_decorator
def foo(): ...

# фабрика декоратора — сначала ВЫЗЫВАЕШЬ функцию с аргументами,
# и ОНА возвращает декоратор, который уже применяется к функции
@router.post("", response_model=PostResponse)
def foo(): ...


in FastAPI
Короткий итог: и router.post(...), и app.get(...) — это функции высшего порядка (точнее, фабрики декораторов: 
функции, возвращающие функции), а сам возвращаемый ими декоратор — ещё одна функция высшего порядка, 
которая принимает твой эндпоинт и кладёт его в скрытый реестр маршрутов, не меняя при этом, 
как сам эндпоинт себя ведёт при вызове.
'''


# same decorator through class

class MyDecorator:
    def __init__(self, func):
        self.func = func       # запомнили функцию

    def __call__(self):
        print("до")
        self.func()
        print("после")

@MyDecorator
def hello():
    print("привет")

hello()
# до
# привет
# после
