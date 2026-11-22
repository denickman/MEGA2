



class Dog:
    def __init__(self, name: str):
        self.name = name

    def bark(self):
        return f'{self.name} bark'


    @classmethod
    def from_string(cls, name: str):
        n = name.split(':')[1]
        # cls(n) — так как cls здесь это Dog (класс, на котором вызван метод), это равносильно Dog('Рекс'),
        # что вызывает __init__ и устанавливает self.name = 'Рекс'
        return cls(n)

    @staticmethod
    def is_valid_name(name: str):
        return len(name) > 0

d = Dog('Bob')
print(d.bark())

Dog.is_valid_name("Рекс")

d2 = Dog.from_string('dog:Рекс')

print(d2.bark())


