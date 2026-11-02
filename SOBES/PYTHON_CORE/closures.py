



def outer(x):
    def inner(y):
        return x + y
    return inner

res1 = outer(1)
print(type(res1))
print(res1(2))



def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c1 = make_counter()
c2 = make_counter()

print(c1())
print(c1())