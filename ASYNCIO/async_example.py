import time
import asyncio


#
# async def main():
#     print("Start of main")
#
# asyncio.run(main())



import asyncio

# Define a coroutine that simulates a time-consuming task
async def fetch_data(delay, id = 1):
    print(f'=========Task # {id}===============')
    print("Fetching data...")
    await asyncio.sleep(delay)  # Simulate an I/O operation with a sleep
    print("Data fetched")
    return {"data": "Some data"}  # Return some data


# Define another coroutine that calls the first coroutine
# async def main():
#     print("Start of main coroutine")
#     task = fetch_data(2)
#     # Await the fetch_data coroutine, pausing execution of main until fetch_data completes
#     result = await task
#     print(f"Received result: {result}")
#     print("End of main coroutine")
#
#
# # Run the main coroutine
# asyncio.run(main())






# async def main2():
#     task1 = fetch_data(2, 1)
#     task2 = fetch_data(3, 2)
#
#     result1 = await task1
#     print(f'Received result: {result1}')
#
#     result2 = await task2
#     print(f'Received result: {result2}')
#
# asyncio.run(main2())







async def fetch_data2(id, sleep_time):
    print(f"====Coroutine {id} starting to fetch data.====")
    await asyncio.sleep(sleep_time)
    return {"id": id, "data": f"Sample data from coroutine {id}"}


async def main2():
    # Create tasks for running coroutines concurrently
    task1 = asyncio.create_task(fetch_data2(1, 1))
    task2 = asyncio.create_task(fetch_data2(2, 2))
    task3 = asyncio.create_task(fetch_data2(3, 3))

    result1 = await task1
    print("1 готов:", result1)
    result2 = await task2
    print("2 готов:", result2)
    result3 = await task3
    print("3 готов:", result3)

    print(result1, result2, result3)


asyncio.run(main2())




'''
Что делает asyncio.gather:

Принимает несколько корутин (или задач) и запускает их все конкурентно. 
Отдельный create_task для каждой не нужен: gather сам оборачивает корутины в задачи.
await asyncio.gather(...) ждёт, пока все завершатся.
Возвращает список результатов в том же порядке, в котором вы передали аргументы, а не в порядке завершения.

Обработка ошибок:

По умолчанию, если одна из корутин бросит исключение, gather сразу пробросит его в await,
а остальные задачи не отменяются, они продолжат работать в фоне.
С return_exceptions=True исключения не пробрасываются, а возвращаются в списке результатов как обычные объекты:
python
results = await asyncio.gather(
    fetch_data(1, 2),
    fetch_data(2, 1),
    return_exceptions=True,
)

gather vs create_task:

gather короче, когда нужно просто запустить пачку и дождаться всех.
create_task нужен, когда хотите обработать результат одной задачи раньше остальных или управлять ей отдельно 
(отменить, проверить статус).
'''

async def main3():
    # Run coroutines concurrently and gather their return values
    results = await asyncio.gather(fetch_data(1, 2), fetch_data(2, 1), fetch_data(3, 3))

    # Process the results
    for result in results:
        print(f"Received result: {result}")



asyncio.run(main3())





'''
Аналог в Swift: это как раз withTaskGroup / withThrowingTaskGroup. 
Та же идея структурированной конкурентности: задачи живут внутри scope, при выходе из него все дождались, 
при ошибке остальные отменяются. Раньше я писал, что в Python такого нет до 3.11, вот это и есть тот самый TaskGroup.


Обработка ошибок: при падении задач TaskGroup бросает ExceptionGroup, ловить её нужно через except*:

python
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(fetch_data(1, 2))
        tg.create_task(failing_coroutine())
except* ValueError as eg:
    print("Ошибки:", eg.exceptions)
    
'''


async def main4():
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for i, sleep_time in enumerate([2, 1, 3], start=1):
            task = tg.create_task(fetch_data(i, sleep_time))
            tasks.append(task)

    # After the Task Group block, all tasks have completed
    results = [task.result() for task in tasks]

    for result in results:
        print(f"Received result: {result}")



asyncio.run(main4())













# def task():
#     print('start')
#     time.sleep(2)
#     print('end')
#
# task()

#
# async def task_async():
#   #  print('start task')
#     await asyncio.sleep(2)
#     print('finish task')
#
# async def main():
#     print('BEGIN MAIN')
#     asyncio.create_task(task_async())
#     print('END MAIN')
#
#     await asyncio.sleep(4)
#
# asyncio.run(main())
