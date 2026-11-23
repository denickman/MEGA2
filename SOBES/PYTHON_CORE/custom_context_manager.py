# 1. Управление ресурсами, которые не файлы
# Любое "открыл → поработал → обязательно закрыл", где закрытие критично даже при ошибке:

'''
Класс с __enter__/__exit__ удобнее, когда:

Нужны дополнительные методы у самого объекта менеджера (не только вход/выход) — например lock.is_locked(),
 transaction.savepoint().
Нужно явно работать с exc_type/exc_val/exc_tb по отдельности, принимая решение на основе конкретного типа ошибки
(как было в примере с isinstance или сравнением типов — в генераторном варианте это тоже возможно через
несколько except, но класс иногда читается нагляднее).
Объект должен быть переиспользуемым/конфигурируемым как обычный класс (с __init__, с состоянием, которое живёт
дольше одного with-блока).
'''




class SuppressException:
    #  def __init__(self, *exceptions, log=True): =
    #  Эта строка говорит: "всё, что передано позиционно (без имени) — собери в кортеж exceptions.
    # А log — это отдельный именованный параметр, причём он обязан передаваться только по имени (log=...),
    # позиционно его передать нельзя."
    def __init__(self, *exceptions, log=True):
        self.exceptions = exceptions   # тут кортеж: (ValueError, ZeroDivisionError)
        self.log = log

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False          # ошибки не было — ничего делать не нужно

        # это проверка "является ли exc_type тем же классом или подклассом (унаследованным классом) от одного из
        # перечисленных в self.exceptions".
        if issubclass(exc_type, self.exceptions):
            if self.log:
                print(f"Suppressed {exc_type.__name__}: {exc_val}")
            return True            # подавляем — ошибка не пролетит наружу

        return False                # не наш тип ошибки — пропускаем как есть


with SuppressException(ValueError, ZeroDivisionError, log=True):
    # Эта строка реально кидает ValueError — Python сам создаёт объект исключения класса ValueError и "выбрасывает" его.
    int("abc")   # ValueError — будет подавлен и залогирован

    #   1 / "строка"   # это TypeError, а не ValueError/ZeroDivisionError!
    #   exc_type будет TypeError. issubclass(TypeError, (ValueError, ZeroDivisionError))
    #   вернёт False — TypeError не входит и не наследник ни от одного из них. Значит выполнится ветка return False в самом низу.

print("Программа продолжает работать")







class Suppress:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("ошибка была:", exc_val)
        return True   # ← говорю Python'у: "замни, я разобрался"

print("строка 1")
with Suppress():
    int("abc")        # ошибка случилась ЗДЕСЬ
    print("эта строка НЕ выполнится — упали ВНУТРИ with")
print("строка 2")     # а это выполнится, потому что __exit__ сказал True

'''
строка 1
ошибка была: invalid literal for int() with base 10: 'abc'
строка 2
'''


class DontSuppress:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("ошибка была:", exc_val)
        return False   # ← говорю Python'у: "не моё дело, пусть падает"

print("строка 1")
with DontSuppress():
    int("abc")
print("строка 2")   # ЭТА СТРОКА НЕ ВЫПОЛНИТСЯ


'''
строка 1
ошибка была: invalid literal for int() with base 10: 'abc'
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 10: 'abc'
'''














class DBConnection:
    def __enter__(self):
        ...
        # self.conn = create_connection()
        # return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.conn.close()   # закроется ВСЕГДА, даже если внутри была ошибка
        # return False
        ...

with DBConnection() as conn:
    conn.execute("SELECT ...")
    # если здесь exception — соединение всё равно закроется


# Это прямо твой FastAPI-кейс: yield в зависимостях (get_db) на самом деле использует ту же идею — try/finally
# вокруг yield — просто через @contextmanager, не через класс.








# 2. Транзакции БД — commit/rollback автоматически
# а здесь на его основе принимается решение commit/rollback.
class Transaction:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()   # всё прошло успешно — сохраняем
        else:
            self.session.rollback() # была ошибка — откатываем
        return False

# with Transaction(session):
#     session.add(user)
#     session.add(order)
    # если на order будет exception — весь блок откатится автоматически








import os

# 3. Временная подмена состояния — потом обязательно вернуть как было
# Частый кейс в тестах: временно подменить конфиг, переменную окружения, sys.path, мокнутую функцию —
# и гарантированно вернуть обратно, что бы внутри блока ни случилось.
class override_env:
    def __init__(self, key, value):
        self.key, self.value = key, value

    def __enter__(self):
        self.old = os.environ.get(self.key)
        os.environ[self.key] = self.value

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.old is None:
            del os.environ[self.key]
        else:
            os.environ[self.key] = self.old
        return False

with override_env("DEBUG", "true"):
    ...
    # run_something()
# после блока переменная окружения точно вернулась к исходной





# 4. Lock / синхронизация (многопоточность, Redis)

class RedisLock:
    def __init__(self, redis, key):
        self.redis, self.key = redis, key

    def __enter__(self):
        self.redis.set(self.key, "locked", nx=True, ex=30)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis.delete(self.key)   # лок освобождается ВСЕГДА
        return False

# with RedisLock(redis_client, "job:42"):
#     process_job()


import time

# 5. Замер времени / профилирование
class timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Took {time.perf_counter() - self.start:.3f}s")
        return False

with timer():
    ...
    # do_heavy_computation()

# 6. Подавление конкретных ошибок — через return True


"""
Вот это ключевой момент, который в твоём коде стоит подчеркнуть: return False (как у тебя) означает "ошибку я 
залогировал, но пусть она пролетает дальше normally" — exception всё равно выбросится наружу после __exit__. 
Если вернуть True — exception проглатывается, дальше код продолжает работать, как будто ничего не было:
"""

class suppress_type_errors:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is TypeError:
            print(f"Подавили TypeError: {exc_val}")
            return True   # проглатываем — наружу ничего не вылетит
        return False      # остальные ошибки пропускаем как есть

with suppress_type_errors():
    int("not a number")  # на самом деле это ValueError, не TypeError — не подавится




# =========================== @contextmanager


from contextlib import contextmanager

'''

@contextmanager (генератор) удобнее, когда:

Логика простая, линейная: "сделать → yield → почистить" — укладывается в одну функцию без состояния, 
которое нужно шарить между несколькими методами.
Не нужно хранить много внутреннего состояния как атрибуты объекта.


Код до yield выполняется один раз при входе в with (аналог __enter__), значение из yield становится тем, 
что попадает в as f, а код после yield — это аналог __exit__, выполняется при выходе из блока. 
Если внутри with-блока случилось исключение — оно "прилетает" прямо в точку yield (как если бы там стоял raise),
 поэтому try/finally нужен, чтобы гарантировать закрытие файла даже при ошибке.
'''

@contextmanager
def file_opener(path, mode='r'):
    f = open(path, mode)
    try:
        yield f          # всё, что ДО yield — это __enter__
                          # то, что передаётся в yield — это значение для "as"
    finally:
        f.close()         # всё, что ПОСЛЕ yield — это __exit__

with file_opener("test.txt") as f:
    print(f.read())



# Транзакция БД (было классом с __enter__/__exit__, теперь так):
@contextmanager
def transaction(session):
    try:
        yield session
        session.commit()        # дошли сюда без ошибок — коммитим
    except Exception:
        session.rollback()      # было исключение — откатываем
        raise                   # важно! пробросить ошибку дальше

# with transaction(session):
#     session.add(user)
#     session.add(order)

# Таймер:
@contextmanager
def timer():
    start = time.perf_counter()
    yield
    print(f"Took {time.perf_counter() - start:.3f}s")

with timer():
    ...
    # do_heavy_computation()

# Подавление ошибок (аналог return True в __exit__):
@contextmanager
def suppress_type_errors():
    try:
        yield
    except TypeError as e:
        print(f"Подавили: {e}")
        # не делаем raise — ошибка "проглочена"

with suppress_type_errors():
    None + 1   # TypeError подавлен, код после with продолжит работать