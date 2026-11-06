
import asyncio
import time



async def cpu_heavy():
    print('cpu begin')
    total = 0
    for i in range(100_000_000):
        total += i    # <-- здесь НЕТ await, ни одного

        # икуственный выигрыш сука тут
        # Но это не ускорит сами вычисления — просто позволит loop'у чередовать работу между task1 и task2,
        # вместо того чтобы домучивать одну до конца. Суммарное время CPU-работы останется тем же
        # (или даже чуть больше из-за накладных расходов на переключение)
        if i % 1_000_000 == 0:
            await asyncio.sleep(0)  # искусственная точка переключения


    print('cpu end')
    return total



async def fetch_data(seconds):
    print('begin request')
    await asyncio.sleep(seconds)
    print('end request')
    # return 666


async def main():
    print(fetch_data)
    start = time.perf_counter()



    # case 1 - concurrent perfromance
    task1 = asyncio.create_task(fetch_data(2))
    task2 = asyncio.create_task(fetch_data(4))

    await task1
    await task2

    # case 2 - asyncio gather
    await asyncio.gather(fetch_data(2), fetch_data(4))





    # concurency does not work here
    # print(await fetch_data(2))
    # print(await fetch_data(3))

    end = time.perf_counter()
    print(f'time to spend: {end - start}')

asyncio.run(main())




async def alternatives():
    tasks = [
        asyncio.create_task(fetch_data(2)),
        asyncio.create_task(fetch_data(4)),
        asyncio.create_task(fetch_data(3)),
    ]

    # wait:
    done, pending = await asyncio.wait(tasks)
    print(f"Завершено: {len(done)}, осталось: {len(pending)}")

    # as_completed:
    for finished_task in asyncio.as_completed(tasks):
        result = await finished_task
        print(f"Готов результат: {result}")

    # TaskGroup:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(fetch_data(2))
        tg.create_task(fetch_data(4))
        tg.create_task(fetch_data(3))


asyncio.run(main())



