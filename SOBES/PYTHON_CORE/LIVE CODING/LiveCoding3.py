
x = 10

print(id(x))

x = x + 1

print(id(x))


print(dir(object))
print(int.__mro__)




import cProfile
print("=====================================")
import cProfile

def slow_function():
    total = 0
    for i in range(10**6):
        total += i ** 2
    return total

cProfile.run('slow_function()')
