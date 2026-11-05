

# functions


def draw_symbol(text: str, count: int) -> str:
    draw = text * count
    return draw

print(draw_symbol(" Hello World! ", 3))



city = 'odesa'

def show_city():
    city = 'medusa'
    print(f'from method: {city}')

show_city()
print(f'from print: {city}')


# Если бы ты хотел именно изменить глобальную переменную изнутри функции, пришлось бы явно это указать через global:
city = 'odesa'

def show_city():
    global city       # говорим: не создавай новую, используй глобальную
    city = 'medusa'
    print(f'from method: {city}')

show_city()
print(f'from print: {city}')





def draw_line(symbol: str, count: int = 3) -> str:
    draw = symbol * count
    print(draw)
    return draw


draw_line("*")



def get_sum(*args):
    print(args)
    print(type(args))
    total_sum = 0
    for el in args:
        total_sum += el
    return total_sum


print(get_sum(1,2,3,4,5))


def print_info(**kwargs):
    print(kwargs)


print_info(name='den', surname='kawa', city='pala')







def calcuate_total(price: float, quantity: int, has_discount: bool = False) -> float:
    total = price * quantity
    if has_discount:
        total -= 10
    return total
















































