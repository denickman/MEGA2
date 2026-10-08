
def calculate_homework(arguments: dict):
    sum_of_grades = 0

    for item in arguments.values():
        sum_of_grades += item

    final_grade = round(sum_of_grades / len(arguments))
    return final_grade

