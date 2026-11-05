

'''
MRO (Method Resolution Order) — это порядок, в котором Python ищет методы и атрибуты при наследовании классов.
Проще говоря: если у класса несколько родителей и у них есть метод с одинаковым именем, MRO определяет,
у какого родителя Python будет искать метод первым.
'''

class Initial:
    def hello(self):
        print("Initial")

class B(Initial):
    def hello(self):
        print("B")

class C(Initial):
    def hello(self):
        print("C")

class D(B, C):
    pass

d = D()
d.hello() # ищет по списку первый попвшиуйся под условие

print(D.mro())


'''
super() без аргументов — это способ обратиться к следующему классу в MRO (Method Resolution Order),
не указывая явно родительский класс.
Проще говоря: super() говорит Python: «Продолжи поиск метода со следующего класса согласно MRO».

super() — не совсем обращение к родительскому классу. Это обращение к следующему классу в MRO.
'''


# duck typing
# Python не нужно знать тип объекта заранее. Он просто пытается выполнить запрошенную операцию во время исполнения.

# Разница в том, что duck typing работает во время выполнения программы (runtime),
# а Protocol помогает проверять совместимость типов ещё до запуска (static type checking).

class Dog:
    def speak(self):
        print("Woof!")


class Cat:
    def speak(self):
        print("Meow!")


def make_sound(animal):
    animal.speak()
















