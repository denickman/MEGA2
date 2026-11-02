

# generators vs list

# list  - store all in memmory
# list - lazy collection
lst = [x*x for x in range(10)]

# generator - almost store nothing
# generator  - lazy creator of values
gen = (x*x for x in range(1000000))

# yield
def my_gen():
    yield 1
    yield 2
    yield 3

# 1. Generator function (с yield)
def gen_func():
    for i in range(3):
        yield i

# 2. Generator expression (без yield)
gen = (i for i in range(3))
# python convert this line in some lie this
def hidden_generator():
    for i in range(3):
        yield i


# Почему второй list(gen) возвращает пустой список? Потому что генератор — одноразовый.

gen = (i for i in range(3))

print(list(gen))  # [0, 1, 2]  — генератор исчерпан
print(list(gen))  # []         — брать уже нечего




result1 = my_gen() # создаёт объект-генератор.
print('----result1-----')
print(result1)
print(type(result1))

# all items in one time
for value in result1:
    print(value)

print('----result2-----')
result1 = my_gen()
# one item at a time
print(next(result1))
print(next(result1))

print('----result3-----')
result1 = my_gen()
print(list(result1))



def gen3():
    yield from [10, 20, 30]

g = gen3()

print(next(g))
print(next(g))
print(next(g))



def coutdown(start: int):
    while start > 0:
        yield start
        start -= 1

gen = coutdown(2)
print(next(gen))
print(next(gen))



# Чтение гигабайтного файла построчно, без загрузки в память
def read_lines(path):
    with open(path) as f:
        for line in f:
            yield line.strip()









import copy

print('----copy-----')
original = [1,2,[3,4]]

# copy.copy
shallow = copy.copy(original)

# copy.deepcopy
deep = copy.deepcopy(original)

original[2][0] = 999

