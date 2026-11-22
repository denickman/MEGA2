'''
В программировании: Python не проверяет тип объекта перед тем, как вызвать у него метод. Ему всё равно,
какого класса объект — главное, чтобы у него был нужный метод/атрибут.


Короче:
duck typing — это сам факт, что Python не требует формальных интерфейсов для полиморфизма.
Protocol — это способ задокументировать и статически проверить этот самый duck typing, не ломая его гибкости (не требуя наследования).
'''



class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Robot:
    def speak(self):
        return "Beep!"

def make_it_speak(thing):
    return thing.speak()   # не важно, что это — лишь бы был .speak()

make_it_speak(Dog())      # "Woof!"
make_it_speak(Cat())      # "Meow!"
make_it_speak(Robot())    # "Beep!"

# make_it_speak не проверяет isinstance(thing, Dog) — он просто вызывает .speak() и верит, что сработает.
# Если у объекта нет .speak() — будет AttributeError, но это выяснится только в момент вызова (runtime), а не заранее.












'''
Protocol (из модуля typing) — "типизированный duck typing"

Проблема: duck typing — это удобно, но IDE/mypy не может подсказать "эй, у этого объекта нет метода .speak()" 
заранее, потому что формально никакого контракта нет.

Protocol — способ формально описать, какой набор методов/атрибутов должен быть у объекта, без наследования. 
Это "структурная типизация" — похоже на интерфейсы в TypeScript/Go.
'''


from typing import Protocol

class Speaker(Protocol):
    def speak(self) -> str:
        ...

def make_it_speak(thing: Speaker) -> str:
    return thing.speak()


# Важный момент: Dog, Cat, Robot из примера выше не обязаны наследоваться от Speaker!
class Dog:          # НЕ наследуется от Speaker
    def speak(self) -> str:
        return "Woof!"

make_it_speak(Dog())   # mypy доволен: у Dog есть speak() -> str, значит подходит под Speaker


'''
Теперь разберём ABC по шагам, медленно

ABC (Abstract Base Class) — это обычное наследование, но с одной фишкой: родительский класс говорит
"у меня есть метод-заглушка, и я запрещаю создавать мои экземпляры, пока наследник не реализует этот метод реально".
 
 

Шаг 1 — зачем это вообще

Представь, что ты пишешь библиотеку и хочешь заставить всех, кто от тебя наследуется,
обязательно реализовать метод speak. Без ABC ты можешь только написать это в комментарии/документации —
Python не проверит это за тебя.
  
Аналогия: ABC — это как собеседование, где тебя пускают только если у тебя есть диплом конкретного вуза 
(формальная принадлежность). Protocol — это как собеседование, где смотрят только на то, умеешь 
ли ты реально делать нужные вещи, неважно, какой диплом у тебя в кармане (или есть ли он вообще).
'''


class Speaker:
    def speak(self) -> str:
        raise NotImplementedError   # "заглушка", но это просто обычный метод

class Dog(Speaker):
    pass   # забыли переопределить speak — но Python это пропустит!

d = Dog()
d.speak()   # упадёт, но только когда реально ВЫЗОВЕМ метод
# Проблема: Dog() создался без ошибки. Ошибка выскочит только при вызове .speak(), и то не сразу.




# Шаг 2 — что добавляет ABC
from abc import ABC, abstractmethod

class Speaker(ABC):
    @abstractmethod
    def speak(self) -> str:
        ...

class Dog(Speaker):
    pass   # забыли переопределить speak

d = Dog()   # TypeError: Can't instantiate abstract class Dog with abstract method speak




# Шаг 3 — а если переопределили как надо
class Dog(Speaker):
    def speak(self) -> str:
        return "Woof!"

d = Dog()        # OK, можно создавать
d.speak()        # "Woof!"


# Шаг 4 — ключевое: ABC требует явного наследования
class Robot:              # НЕ наследуется от Speaker!
    def speak(self) -> str:
        return "Beep!"

isinstance(Robot(), Speaker)   # False! Хотя метод speak() есть и сигнатура та же

# С Protocol было бы наоборот:
make_it_speak(Robot())   # mypy: OK! Наследование не нужно, важна только форма