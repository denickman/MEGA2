from enum import unique

# print('hello', input('input your name: '))
# name = input('input your name: ')
# print(name)
#
# print(len(name))
# print(type(name))
# print(id(name))


# print(2*3)
# print(2**2)
#
# print(10 / 3)
# print(10 // 3)
#
#
# ranga = range(5)
# print(ranga)

# for i in range:
#     print(i)

# for i in range(1, 6):
#     text = 'hello'
#     print(i, text)



# count = 0
# while count < 5:
#     print(count)
#     count += 1


# result = 0
#
# for i in range(3):
#     num = int(input('enter a number: '))
#     if num < 0:
#         break
#         # continue
#     result += num
#
# print(f'Final result is: {result}')





# ============== string ============================


name = 'denis yaremenko'

print('is' in name)


phone_number = '+380974322561'


print(name[1:-2])

len(name)
print(name.capitalize())
print(name.lower())
print(name.upper())

if phone_number.strip().startswith('+3'):
    print(phone_number[3:])

if phone_number.strip().endswith('1'):
    print(phone_number[:-1])




phone_number = phone_number.strip().replace('+', 'xxx')
print(phone_number)

print(phone_number.count('x'))


# ============== list ============================



l = ['abc', 1, 2, 3, 'cde']

print(type(l))
print(len(l))
print(id(l))
print(1 in l)



print(list(range(10)))

# print(sum(l))
# print(min(l))
# print(max(l))


l.insert(1, 2)
l.insert(0, 'kawabung')

l.append(1)
l.append('hello')

print(l)

deleted = l.pop(1)
print(deleted)
print(l)


l2 = [1, 7, 4, 3, 6, 4,9, 3]
l2.sort(reverse=True)
# l2_sorted = sorted(l2, reverse=True)
print(l2)

for index, el in enumerate(l2):
    print(index, el)


string = 'i am anal fucker'
list_string = string.split(' ')
print(list_string)

ip = '127.0.0.1'
print(ip.split('.'))

string_to_list = ' '.join(list_string)
print(string_to_list)

empty_numbers = []

for i in range(5):
    empty_numbers.append(i)

print(empty_numbers)

numbers = [i for i in range(5)]





# ============== dict ============================


author = {
    'name': 'denis yaremenko',
    'age': 20
}

print(author.get('name'))
print(author['name'])

print(author.keys())
print(author.values())

for key in author:
    print(f'Key: {key}, Value: {author[key]}')


for pair in author.items():
    print(f'tuple: {pair}')



# ===== tuples ======

my_tuple = ('a', 'b', 'c')


a,b,c = my_tuple
print(a)

# ===== sets ======
numbers = {101, 102, 103}

lang = ['c++', 'js', 'swift', 'python']
unique_lang = set(lang)
print(unique_lang)

numbers.remove(101)
numbers.add(666)


my_set1 = {1, 2, 3, 4, 5}
my_set2 = {3,4,5,6,7,8}

# unite
print(my_set1 | my_set2)

# cross
print(my_set1 & my_set2)

# diff
print(my_set1 - my_set2)

# simmetry diff
print(my_set1 ^ my_set2)






