

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def say_hello(self, to_name: str):
        print(f'hello {to_name}')

user1 = User('den', 20)

user1.say_hello("Alex")
print(user1.__dict__)




class BankAccount:
    def __init__(self, balance: int):
        self.__balance = balance


    def deposit(self, amount: int):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance



bank = BankAccount(100)
print('BEFORE')
print(bank.__balance)
bank.__balance = 10000

print('AFTER')
print(bank.__balance)