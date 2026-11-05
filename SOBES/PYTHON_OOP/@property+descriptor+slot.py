


class User:
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name # геттер: срабатывает при чтении user.name

    @name.setter
    def name(self, value):
        if not  value:
            raise ValueError("Name cannot be empty")
        self._name = value.capitalize()

    @name.deleter
    def name(self):
        del self._name






