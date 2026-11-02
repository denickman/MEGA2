



# a = []  он создаёт список [] один раз при создании функции. И потом при каждом вызове использует тот же самый список.
# Никогда не используй изменяемые объекты (list, dict, set) в качестве значений по умолчанию.

def add_item(item, a=[]):
    a.append(item)
    return a


value1 = add_item((1))
value2 = add_item((2))
value3 = add_item((3))

print(value1)
print(value2)
print(value3)

# Как правильно делать
def add_item(item, a=None):
    if a is None:
        a = []
    a.append(item)
    return a