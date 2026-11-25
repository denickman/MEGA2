



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


print("========================")

import asyncio
import time

async def fetch_data(seconds: int, id: int):
    print(f"Begin request task: {id}")
    await asyncio.sleep(seconds)
    print(f"End request task: {id}")

async def main():
    start = time.perf_counter()
    print(await fetch_data(2, 1))
    print(await fetch_data(4, 2))
    end = time.perf_counter() - start
    print("Time taken: ", end)


# asyncio.run(main())

async def main_super():
    start = time.perf_counter()

    task1 = asyncio.create_task(fetch_data(2, 1))
    task2 = asyncio.create_task(fetch_data(4, 2))

    await task1
    await task2

    end = time.perf_counter() - start
    print("Time taken: ", end)


# asyncio.run(main_super())


async def main_gather():
    start = time.perf_counter()
    await asyncio.gather(fetch_data(2, 1), fetch_data(4, 2))
    end = time.perf_counter() - start
    print("Time taken: ", end)

asyncio.run(main_gather())











