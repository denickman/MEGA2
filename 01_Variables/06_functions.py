

def get_average_temperature() -> float:
    with open('files/temperature.txt') as f:
        data = f.readlines()
        values = data[1:]
        values = [float(i) for i in values]

        average_local = sum(values) / len(values)

    return average_local

avarage = get_average_temperature()
print(avarage)