




def get_age() -> str:
    return 25   # на самом деле возвращает int, не str!

print(get_age())   # 25 — прекрасно работает, Python не ругается!
print(type(get_age()))




# try:
#     width = float(input("enter width: "))
#     height = float(input("enter height: "))
#
#     if width == height:
#         print("square")
#         exit("will break the programm")
#
#     area = width * height
#
#     print(area)
# except (ValueError, TypeError):
#     print("Please enter numeric values")



try:
    total_value = float(input("Enter total value: "))
    value = float(input("Enter value: "))

    percentage = value / total_value * 100
    print(f"That is {percentage}%")

except ValueError:
    print("You did not enter a number")


