

import time


# deco

def deco_time(func):
    def wrapper(*args, **kwargs):
        print('begin')
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('end')
        print('=========')
        print(f'{func.__name__} took {end - start} seconds')
        return result
    return wrapper


    # def wrapper():
    #     print('begin')
    #     func()
    #     print('end')



@deco_time
def load_file():
    print('load file')
    time.sleep(2)


load_file()