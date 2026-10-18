import calendar

print('=========================')
print('welcome to the supa mega calendar\n')

year = int(input('Enter a year: '))
month = int(input('Enter a month: '))

print(calendar.month(year, month))

print('Good luck!')