'''
try:
    # код, который может вызвать ошибку
except SomeError:
    # что делать, если ошибка произошла
else:
    # выполнится ТОЛЬКО если ошибки НЕ было
finally:
    # выполнится ВСЕГДА (была ошибка или нет)
'''


# try + except
try:
    number = int(input('enter a number: '))
except ValueError:
    print('this is not a number')

# try + except + else
try:
    number = int(input('enter a number: '))
except ValueError:
    print('this is not a number')
else:
    print('this is a number')




# try + finally
try:
    file = open('data.txt')
    content = file.read()
finally:
    file.close()

# full
try:
    number = int(input('enter a number: '))
    result = 10 / number
except ZeroDivisionError:
    print('division by zero')
except ValueError:
    print('this is not a number')
else:
    print('this is a number')
finally:
    print('this is a number')










