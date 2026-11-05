



try:
    number = int(input('enter a number: '))
    print(10 / number)
except ZeroDivisionError:
    print('division by zero')
except ValueError:
    print('invalid input')



# if you want to catch any error

try:
    number = int(input('enter a number: '))
    print(10 / number)
except Exception as e:
    print(e)
else:
    print('a mistake did not occur')
finally:
    print('print forever')


















































