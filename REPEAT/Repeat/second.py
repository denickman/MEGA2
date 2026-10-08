
from grade_average_service import *

# def my_function():
#     print('inside my function')
#
#
# my_function()
#
#
# def print_my_name(name: str, surname: str):
#     print(f'print my name is: {name}')
#
#
# print_my_name('den')
#
#
# def print_numbers(h_num: int, l_num: int):
#     print(h_num, l_num)
#
#
#
# def user_dict(name: str, surname: str, age: int):
#     dict = {'name': name, 'surname': surname, 'age': age}
#
#     return dict



homework_grades = {
    'h1': 100,
    'h2': 25,
    'h3': 45,
    'h4': 67,
    'h5': 69,
}






check_homework = calculate_homework(homework_grades)
print("----results----")
print(check_homework)


