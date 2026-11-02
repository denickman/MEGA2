# Like computed property in swift

class User:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):          # это "get" — вызывается при ЧТЕНИИ user.name
        return self._name

    @name.setter
    def name(self, value):   # это "set" — вызывается при ЗАПИСИ user.name = ...
        self._name = value.capitalize()


u = User("den")
print(u.name)      # "den" — сработал геттер (@property)
u.name = "maria"    # сработал сеттер (@name.setter)
print(u.name)        # "Maria"