
'''

Контекстный менеджер (Context Manager) — это механизм Python, который автоматически управляет началом и завершением
определённой операции.

Проще говоря: он позволяет выполнить какой-то код, а затем гарантированно выполнить завершающие действия,
аже если во время выполнения произошла ошибка.

Самый знакомый пример — with open().

Context Manager управляет жизненным циклом операции: начало → выполнение → завершение.

with запускает этот механизм.
Класс использует __enter__ и __exit__.
@contextmanager позволяет реализовать то же самое через функцию и yield.
finally гарантирует выполнение завершающего кода даже при исключениях.

«Контекстный менеджер — это протокол из
__
enter
__
и
__
exit
__
, который
гарантирует освобождение ресурса даже при исключении. Под капотом это тот
же try/finally, но переиспользуемый и декларативный. Если состояние
простое, пишу через @contextmanager и генератор с try/finally вокруг yield.
»

'''


# custom context manager

class Transaction:
    def __enter__(self):
        print("Begin")
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("Commit")
        else:
            print("Rollback")
            return False



from contextlib import contextmanager

@contextmanager
def open_resouce(path: str):
    f = open(path)
    try:
        yield f
    finally:
        f.close()