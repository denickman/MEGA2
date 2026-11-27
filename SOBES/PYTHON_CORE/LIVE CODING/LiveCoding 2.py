


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


















