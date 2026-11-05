# ABC (Abstract Base Class)

# ABC — наследуйся от меня и реализуй необходимые методы.
# Protocol — мне неважно, от кого ты наследуешься, главное, чтобы у тебя были нужные методы.

# Разница в том, что duck typing работает во время выполнения программы (runtime),
# а Protocol помогает проверять совместимость типов ещё до запуска (static type checking).
# Без Protocol статический анализатор может не обнаружить проблему, если тип аргумента никак не указан.

'''
ABC (Abstract Base Class) — номинальная типизация
Обязывает через явное наследование. Класс обязан унаследоваться от ABC, иначе Python даже не даст его создать


Protocol — структурная типизация (duck typing)
Никакого наследования не требуется вообще. Если у класса есть метод с нужным именем и сигнатурой —
он автоматически подходит, даже не зная о существовании протокола.
'''



from abc import ABC, abstractmethod

class Speakable(ABC):
    @abstractmethod
    def speak(self): ...

class Dog(Speakable):   # ОБЯЗАТЕЛЬНО явное наследование
    def speak(self):
        print("Woof")

class Cat:               # НЕ наследуется от Speakable
    def speak(self):
        print("Meow")

Dog()   # OK
Cat()   # OK, но Cat никак не связан с Speakable

d = Dog()
isinstance(d, Speakable)   # True
c = Cat()
isinstance(c, Speakable)   # False — хотя структурно Cat точно такой же!


class Dog(Speakable):
    pass

Dog()  # TypeError: Can't instantiate abstract class Dog with abstract method speak


# protocol


from typing import Protocol

from typing import Protocol

class Speakable(Protocol):
    def speak(self): ...

class Dog:                      # никак не связан с Speakable
    def speak(self):
        print("Woof")

class Cat:                      # тоже никак не связан
    def speak(self):
        print("Meow")

def make_sound(animal: Speakable):
    animal.speak()

make_sound(Dog())   # работает
make_sound(Cat())   # тоже работает — оба структурно подходят












