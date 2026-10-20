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












async def set_future_result(future, value):
    await asyncio.sleep(2)
    # Устанавливаем результат future
    future.set_result(value)
    print(f"Set the future's result to: {value}")


async def main5():
    # Создаём future
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    # Запускаем задачу, которая позже положит в future результат
    asyncio.create_task(set_future_result(future, "Future result is ready"))

    # Ждём результат
    result = await future
    print(f"Received the future's result: {result}")


asyncio.run(main5())

'''
Что такое Future

Future это пустая "коробочка" под результат, который появится позже. 
Сам по себе он ничего не вычисляет. У него два состояния: результата ещё нет или он уже положен (через set_result, 
либо ошибка через set_exception).

Как это работает здесь:

main создаёт пустой future и запускает вторую задачу set_future_result.
await future приостанавливает main. Event loop свободен и выполняет другую задачу.
Через 2 секунды set_future_result вызывает future.set_result(...).
Это "будит" main, и await future возвращает значение.

То есть один участок кода ждёт, а другой выполняет, и Future связывает их.

Отличие от Task: Task это Future, у которого результат появляется сам, когда завершится корутина. 
Здесь же результат кладёшь вручную. В обычном коде ты почти не создаёшь Future вручную, он нужен для "мостов" 
между callback-кодом и async/await.

Аналог в Swift

Самый близкий это withCheckedContinuation:

swift
func main() async {
    let result = await withCheckedContinuation { continuation in
        // Позже, откуда-то извне:
        DispatchQueue.global().asyncAfter(deadline: .now() + 2) {
            continuation.resume(returning: "Future result is ready")
        }
    }
    print("Received the future's result: \(result)")
}

Соответствие:

Python	Swift
loop.create_future()	withCheckedContinuation { ... }
future.set_result(value)	continuation.resume(returning: value)
future.set_exception(e)	continuation.resume(throwing: e) (withCheckedThrowingContinuation)
await future	await withCheckedContinuation

Разница в том, что в Python Future это отдельный объект, который можно передавать куда угодно, 
а в Swift continuation живёт внутри замыкания. Правило у обоих одно: результат можно положить только один раз.

Если искать другие аналоги: Future из Combine (publisher с одним значением) 
и Promise из PromiseKit тоже похожи по идее, но для async/await в Swift основной мост это continuation.

'''









# Общая переменная
shared_resource = 0

# Асинхронный замок
lock = asyncio.Lock()


async def modify_shared_resource():
    global shared_resource
    async with lock:
        # Критическая секция начинается
        print(f"Resource before modification: {shared_resource}")
        shared_resource += 1                 # меняем общий ресурс
        await asyncio.sleep(1)               # имитация IO-операции
        print(f"Resource after modification: {shared_resource}")
        # Критическая секция заканчивается


async def main6():
    await asyncio.gather(*(modify_shared_resource() for _ in range(5)))


asyncio.run(main6())


'''
Что здесь происходит
shared_resource это общая переменная, которую хотят менять сразу 5 задач.
asyncio.gather(...) запускает 5 копий modify_shared_resource одновременно.
async with lock: это замок: внутри блока может находиться только одна задача. 
Остальные ждут на входе. Когда первая выходит, замок берёт следующая.
global нужен, чтобы менять переменную модуля, а не создавать локальную.
Зачем замок, если поток один

В asyncio всё выполняется в одном потоке, и кажется, 
что гонок данных быть не может. Но задача отдаёт управление на каждом await. 
В коде выше внутри блока есть await asyncio.sleep(1): пока одна задача спит, 
loop запускает другую, и та лезет в тот же ресурс.

Без замка вывод был бы такой:

before: 0
before: 1
before: 2
before: 3
before: 4
after: 5
after: 5
after: 5
after: 5
after: 5

Все пять задач успевают войти, и каждая видит чужие изменения. 
С замком каждая задача проходит блок целиком (до await и после него), и состояние остаётся согласованным.

Итого: гонки в asyncio возможны только там, 
где между чтением и записью стоит await. Если await внутри нет, замок не нужен.

Обрати внимание: asyncio.Lock нужно использовать именно с async with, а не with, 
и он не потокобезопасный. Для обычных потоков есть threading.Lock.

Аналог в Swift

Первая мысль это actor, и идея похожая (защита общего состояния), но есть важное отличие:

swift
actor Counter {
    var value = 0

    func modify() async {
        print("before: \(value)")
        value += 1
        try? await Task.sleep(for: .seconds(1))
        print("after: \(value)")
    }
}

Actor защищает от одновременного доступа, но он реентерабельный: 
на await он отпускает изоляцию, и другой вызов может зайти внутрь, 
пока первый спит. Поэтому этот код в Swift выведет то же, что asyncio без замка.
'''






async def access_resource(semaphore, resource_id):
    async with semaphore:
        # Имитация доступа к ограниченному ресурсу
        print(f"Accessing resource {resource_id}")
        await asyncio.sleep(1)  # имитация работы с ресурсом
        print(f"Releasing resource {resource_id}")


async def main7():
    semaphore = asyncio.Semaphore(2)  # разрешаем 2 одновременных доступа
    await asyncio.gather(*(access_resource(semaphore, i) for i in range(5)))


asyncio.run(main7())


'''
Вывод (занимает около 3 секунд):

Accessing resource 0
Accessing resource 1
Releasing resource 0
Releasing resource 1
Accessing resource 2
Accessing resource 3
Releasing resource 2
Releasing resource 3
Accessing resource 4
Releasing resource 4
Что такое Semaphore

Semaphore это замок, который пускает внутрь не одну задачу, а N одновременно. Внутри у него счётчик свободных мест:

Semaphore(2): изначально 2 места.
async with semaphore: занимает место (счётчик минус 1). Если мест нет, задача ждёт.
Выход из блока освобождает место (счётчик плюс 1), и следующая ожидающая задача заходит.

Здесь запущено 5 задач, но одновременно работают только 2. Поэтому они идут парами: (0, 1), потом (2, 3), потом 4.

Lock против Semaphore
	Lock	Semaphore(N)
Сколько задач внутри	ровно 1	до N
Для чего	защитить общие данные	ограничить параллелизм

Lock по сути это Semaphore(1).

Где пригодится у тебя

Типичный случай для твоего FastAPI и AI-проекта: ограничить число одновременных запросов к внешнему API (LLM, например, лимит 5 запросов одновременно), чтобы не упереться в rate limit:

python
llm_semaphore = asyncio.Semaphore(5)

async def call_llm(prompt: str):
    async with llm_semaphore:
        return await client.generate(prompt)

Можно запустить 100 задач через gather, а наружу одновременно уйдёт не больше 5 запросов.

Аналог в Swift

Готового async-семафора в стандартной библиотеке нет. DispatchSemaphore блокирует поток, и использовать его внутри async кода нельзя (риск дедлока).

'''