



from typing import Annotated, get_type_hints

def f(age: Annotated[int, "в годах"]): ...

print(get_type_hints(f, include_extras=True))
# {'age': typing.Annotated[int, 'в годах']}





print("-----------------------------------")



first_name = 'Den'
print(f"hello {first_name}")


sentence = 'Hi {} {}'

last_name = 'Remen'

print(sentence.format(first_name, last_name))

print('----- Strings -----')

print('-----case 1 -----')
print(f'hi {first_name} {last_name}. I hoe you are doing well!')

print('-----case 2 -----')
print(f'hi {first_name} {last_name}. '
      f'I hoe you are doing well!')

# print('-----case 3 -----')
# days = input('How many days until your birthdays? ')
# print(type(days))
# print(type(round(int(days))))
# print(round(days/7, 2))
# print(int(days)/7)



print('----- Sets -----')


my_set = {1, 2, 3, 4, 5, 1, 2, 5}
my_set.discard(2)
# print(my_set)


# add element
my_set.add(12)

# remove all elements from set
# my_set.clear()

print(f'length of: {len(my_set)}') # automaticall remove duplicates

for x in my_set:
    print(x)


print('----- Tuples -----')

# tuples are unchangeble

my_tuple = (1, 2, 3, 4, 5, 6, 7)
print(my_tuple)
print(my_tuple[1])


print('----- Dictionaries -----')

user_dict = {
    'username':'den',
    'name': 'eric',
    'age': 30,
}

user_dict['age'] = 40
print(user_dict.get('username'))



for key,value in user_dict.items():
    print(f'key: {key}, value: {value}')


print('----- chceck delete -----')

user_dict2 = user_dict
user_dict2.pop('username')

print(user_dict2)

# deep copy
import copy
user_dict2 = copy.deepcopy(user_dict)









print('-----Range / Loops-----')
for x in range(3, 6):
    print(x)


days = ['sun', 'mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun']

for day in days:
    print(f'Happy {day}!')


print('---while loop-----')

i = 0

while i < 5:
    i += 1
    if i == 3:
         continue
    print(i)

    if i == 4:
        break

else:
    print('i is now larger or equal to 5')











