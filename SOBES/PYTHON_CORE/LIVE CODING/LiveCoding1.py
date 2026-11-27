


# o(n2) brute force
def find_summands(numbers: list[int], target: int) -> tuple[int, int]:
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return numbers[i], numbers[j]





# o(n) - hash table

def find_summands_2(numbers: list[int], target: int) -> tuple[int, int]:
    seen = {}  # число -> его индекс

    for i, num in enumerate(numbers):
        needed = target - num
        # in для словаря по умолчанию всегда проверяет именно ключи, а не значения — это важное правило Python
        if needed in seen:
            return (seen[needed], i)
        seen[num] = i


'''

numbers = [15, 2, 11, 7]  # несортированный, в случайном порядке
target = 9


i = 0 
num = 15 
needed = 9 - 15 = -6 -> {15: 0}

i = 1
num  = 2
needed = 9 - 2 = 7 -> {15: 0, 2: 1}

i = 2
num = 11 
needed = 9 - 11 = -2 -> {15: 0, 2: 1, 11: 2}

i = 3 
num = 7 
needed = 9 - 7 = 2 -> ДА, seen[2]=1

'''







test1 = find_summands(numbers=[1, 2, 3, 4, 5, 6, 7], target=7)
print(test1)

def find_summands_3(numbers: list[int], target: int) -> tuple[int, int]:
    seen = set()

    for num in numbers:
        needed = target - num
        if needed in seen:
            return (needed, num)

        seen.add(num)






# ==============================================================================================================

def f(x, l=[]):
    l.append(x)
    print(l)

l = [1]

f(10)
f(10)
f(10, l) # вместо дефолтного списка используется ТО, что передали как аргумент
f(10)


# None — безопасный immutable дефолт, а настоящий пустой список создаётся заново при каждом вызове внутри тела функции,
# если l не передан.
def f(x, l=None):
    if l is None:
        l = []

    l.append(x)
    print(l)










# ==============================================================================================================



# time.time() — реальное "настенное" время (wall clock)
# time.monotonic() — "часы, которые только идут вперёд"
# time.perf_counter() — то же самое, что monotonic, но ТОЧНЕЕ


# perf_counter даёт гарантированно самое высокое разрешение, доступное на конкретной системе
# (может быть наносекунды), специально предназначен именно для измерения коротких интервалов времени выполнения кода
# (отсюда и название — "счётчик производительности").
#
# monotonic() тоже не идёт назад, но его точность не гарантируется быть максимальной —
# на некоторых платформах разрешение может быть грубее (например, миллисекунды вместо наносекунд),
# потому что monotonic создавался больше для общих целей ("сколько времени прошло вообще"), а не специально
# ля микро-замеров производительности кода.


# Практический вывод
# Нужно узнать текущую дату/время ("какое сегодня число", записать timestamp в БД) → time.time() (или лучше datetime.now())
#
#
# Нужен таймаут / "не прошло ли N секунд" в общей логике приложения → time.monotonic()
#
#
# Нужно измерить, сколько заняла функция/блок кода (бенчмарк, профилирование, как в нашем декораторе) → time.perf_counter()
# — максимальная точность именно для этой задачи


# decorator with time log
import time
from functools import wraps
import random

def timer(func):
    # @functools.wraps(func) vs @wraps(func) — разница только в способе импорта, функция одна и та же
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Start:")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} выполнилась за {end - start:.4f} сек")
        print("End:")

        return result
    return wrapper


@timer
def slow_func(n):
    total = 0
    for i in range(n):
        total += i
    return total

slow_func(1000)








# ===========================================3x level decorator=================================================
import functools

def retry(n):
    def decorator(func):
        # @functools.wraps(func) vs @wraps(func) — разница только в способе импорта, функция одна и та же
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, n+1):
                try:
                    return func(*args, **kwargs)
                # Голый raise (без указания типа ошибки) работает только внутри блока except, потому что он перевыбрасывает то исключение,
                # которое СЕЙЧАС обрабатывается Python-ом.
                except Exception as e:
                    if attempt == n:
                        # Голый raise внутри блока except означает:
                        # "перевыбросить то исключение, которое СЕЙЧАС обрабатывается"
                        raise
                    print(f"Попытка {attempt} не удалась: {e}, пробуем снова...")
        return wrapper
    return decorator



print("======retry decorator=======")

@retry(3)
def unstable():
    randoma = random.random()
    print(f"RANDOM: {randoma}")

    if randoma < 0.7:
        raise ValueError("Something fucking off")
    return 'success!'

result = unstable()
print(result)









# ============================================BUGGGGS==================================================================

def get_first_matching_object(predicate, objects=[]):
    matching_objects = (obj for obj in objects if predicate(object))
    if matching_objects:
        object = matching_objects[0]
        return object
    else:
        return None

# Problems
# objects=[] — та самая mutable default argument ловушка, которую разбирали

# matching_objects = (obj for obj in objects if predicate(obj)) это генератор, а не список
# Круглые скобки (...) создают генератор (generator expression), а не список. Это ключевая проблема,
# из-за неё код сломан в двух местах:

# if matching_objects: — генератор всегда truthy (истинный), независимо от того,
# даст ли он хоть один элемент или нет! Генератор — это просто объект-итератор, и сам факт его существования —
# всегда "правда", Python не умеет "заглянуть внутрь" генератора, чтобы проверить, есть ли там элементы, без того,
# чтобы начать их потреблять.


# matching_objects[0] — у генераторов нет индексации. Это вызовет ошибку:
# TypeError: 'generator' object is not subscriptable

# object = matching_objects[0] — затенение встроенного имени
# object — это встроенный тип в Python (базовый класс всех объектов). Называть переменную так же — плохая практика:
# внутри этой функции (и в этой области видимости) object теперь указывает на твою переменную, а не на встроенный тип,
# что может сломать код, если где-то ниже понадобится настоящий object (например, isinstance(x, object)).


# решение исправеление

def get_first_matching_object(predicate, objects=None):
    if objects is None:
        objects = []

    for obj in objects:
        if predicate(obj):
            return obj
    return None


'''
Простой цикл вместо генератора — не нужно вообще городить generator expression для такой задачи. 
Проходим по objects, и как только находим первый элемент, подходящий под predicate — сразу return его. 
Если прошли весь список и ничего не подошло — return None в конце.

Нет проблемы с "пустой генератор truthy" — обычный for просто естественно завершается, если ничего не подошло, 
и код доходит до return None.

objects=None + проверка внутри — классический безопасный паттерн вместо mutable default (из нашего прошлого разговора).
'''






# Альтернатива — через next() с генератором (если хочешь именно "питонично" и компактно)
def get_first_matching_object(predicate, objects=None):
    if objects is None:
        objects = []
    return next((obj for obj in objects if predicate(obj)), None)


'''
Тут генератор используется правильно — next() умеет забирать первый элемент из генератора, и у него есть второй аргумент 
(None) — значение по умолчанию, которое вернётся, если генератор пуст (StopIteration перехватывается автоматически). 
Это однострочный эквивалент твоего исходного замысла, без багов.
'''



numbers = [1, 3, 5, 8, 10, 12]

result = get_first_matching_object(lambda x: x % 2 == 0, numbers)
print(result)  # 8 — первое чётное число

result = get_first_matching_object(lambda x: x > 100, numbers)
print(result)  # None — ничего не подошло




# ==============================================================================================================

# написать генератор - принимающий на вход массив - и итерируеца по этому массиву цикличиески /
# то есть проход по всем элементам массива до бекконечности


def cyclic(items:list[int]):
    while True:
        for item in items:
            yield item

gen = cyclic(numbers)
print(next(gen))
print(next(gen))



# ==============================================================================================================

# более продвинутая версия генератора

# items: Iterable[T] вместо items: list — принимает ЛЮБОЙ итерируемый объект, не только список
# Функция теперь может принять что угодно, что можно перебрать: список, кортеж, множество, генератор, диапазон (range),
# результат другого генератора

'''


Типизация -> Generator[T, None, None]
T — тип того, что генератор отдаёт через yield (в нашем случае — тип элементов массива)
None (второй) — тип того, что можно отправить генератору через .send() (тут не используется, поэтому None)
None (третий) — тип значения, которое генератор возвращает при завершении через return (тут генератор не возвращает 
ничего явно, поэтому None)


Да, именно так — все эти типы реализуют Iterable-протокол

Iterable в Python — это не какой-то один конкретный тип, а протокол (контракт): "любой объект, у которого есть 
метод __iter__, который возвращает итератор". Python не проверяет "является ли это list, tuple или set" — 
он просто проверяет, умеет ли объект отдавать себя по одному элементу через for.

[1, 2, 3].__iter__          # у list ЕСТЬ __iter__ → Iterable
(1, 2, 3).__iter__          # у tuple ЕСТЬ __iter__ → Iterable
{1, 2, 3}.__iter__          # у set ЕСТЬ __iter__ → Iterable
range(5).__iter__           # у range ЕСТЬ __iter__ → Iterable
(x for x in [1,2]).__iter__ # у генератора ЕСТЬ __iter__ → Iterable
"hello".__iter__            # у строки ЕСТЬ __iter__ → Iterable (!)



from typing import Iterable

print(isinstance([1, 2, 3], Iterable))        # True
print(isinstance((1, 2, 3), Iterable))        # True
print(isinstance({1, 2, 3}, Iterable))        # True
print(isinstance(range(5), Iterable))         # True
print(isinstance("hello", Iterable))          # True
print(isinstance(42, Iterable))               # False — число нельзя перебрать циклом
'''


from typing import Iterable, Generator, TypeVar
T = TypeVar("T")

def super_gen(items: Iterable[T]) -> Generator[T, None, None]:
    # list(generator) работает — забирает ВСЕ элементы генератора в реальный список
    items = list(items)
    while items:
        for i in items:
            yield i









# ==============================================================================================================










