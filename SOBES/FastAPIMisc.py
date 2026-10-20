
'''

run_in_threadpool — для блокирующих (не CPU-bound) операций
FastAPI/Starlette имеет встроенную функцию, которая выполняет синхронный код в отдельном потоке,
не блокируя event loop:

Это полезно для блокирующего I/O (синхронный драйвер БД, файловые операции, старые синхронные HTTP-клиенты) —
поток ждёт I/O, но не держит GIL всё время, поэтому event loop продолжает работать.
'''

from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
import time

app = FastAPI()

def blocking_io():
    time.sleep(2)  # имитация блокирующей операции (I/O, синхронная либа)
    return "done"

@app.get("/endpoint")
async def endpoint():
    result = await run_in_threadpool(blocking_io)
    return {"result": result}



'''
Но для CPU-bound задач потоки не помогают

Из-за GIL (Global Interpreter Lock) только один поток может выполнять Python-байткод одновременно. 
Если задача — это чистые вычисления (не I/O, а, например, обработка изображения, тяжёлая математика), 
то запуск в потоке всё равно заблокирует весь процесс, включая event loop, потому что GIL не отпускается во время CPU-вычислений.

'''

def cpu_heavy():
    total = 0
    for i in range(10**9):
        total += i
    return total

@app.get("/cpu-endpoint")
async def endpoint():
    # Это НЕ спасёт event loop — GIL всё равно заблокирует остальные запросы
    result = await run_in_threadpool(cpu_heavy)
    return {"result": result}

'''
Для настоящего CPU-bound — нужен отдельный процесс
Правильное решение — ProcessPoolExecutor, который реально создаёт отдельный процесс (со своим GIL), а не поток:

Здесь run_in_executor с явно переданным ProcessPoolExecutor выносит вычисление в отдельный процесс — 
event loop остаётся свободным и может обрабатывать другие запросы, пока тяжёлое вычисление идёт параллельно на другом ядре CPU.
'''

from concurrent.futures import ProcessPoolExecutor
import asyncio

app = FastAPI()
process_pool = ProcessPoolExecutor()

def cpu_heavy(n):
    total = 0
    for i in range(n):
        total += i
    return total

@app.get("/cpu-endpoint")
async def endpoint():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(process_pool, cpu_heavy, 10**9)
    return {"result": result}








'''
GIL (Global Interpreter Lock)

Это механизм в CPython (стандартной реализации Python), который гарантирует, что только один поток может выполнять
Python-байткод в любой момент времени, даже если у тебя несколько потоков и несколько ядер CPU.

Проще говоря: внутри одного процесса Python сколько бы потоков ты ни создал, реально одновременно
(в один конкретный момент времени) работает только один — остальные ждут своей очереди на "замок" (lock).

Зачем он вообще существует

CPython управляет памятью через подсчёт ссылок (reference counting) — каждый объект знает, сколько у него "ссылок" (
переменных, которые на него указывают), и когда счётчик доходит до нуля — объект удаляется сборщиком мусора.
Если бы несколько потоков одновременно меняли этот счётчик без защиты — возникали бы race conditions и порча памяти.
GIL — это "простое" (хоть и спорное) решение этой проблемы: просто не давать потокам выполняться по-настоящему параллельно.



Когда GIL НЕ мешает — I/O операции

Во время I/O (сеть, диск, time.sleep) поток отпускает GIL, пока ждёт ответа от ОС/сети/диска. 
Поэтому для I/O-bound задач потоки в Python всё ещё полезны — пока один поток "спит"/ждёт сеть, другой может взять GIL и выполняться.

Это как раз объясняет, почему run_in_threadpool работает для I/O, но бесполезен для CPU-вычислений — 
там GIL просто не отпускается, пока идёт расчёт.

Как обходят GIL
Отдельные процессы (multiprocessing, ProcessPoolExecutor) — у каждого процесса свой интерпретатор, 
свой GIL, реальный параллелизм на разных ядрах
Библиотеки на C (NumPy, и т.д.) часто отпускают GIL внутри тяжёлых C-операций

В Python 3.13+ появился экспериментальный режим “free-threaded” Python (PEP 703) — сборка интерпретатора без GIL вообще, 
но это пока не дефолт

'''

import threading
import time

def cpu_heavy():
    total = 0
    for i in range(10**8):
        total += i

start = time.time()

t1 = threading.Thread(target=cpu_heavy)
t2 = threading.Thread(target=cpu_heavy)
t1.start()
t2.start()
t1.join()
t2.join()

print(time.time() - start)
# Ожидаешь ~2x ускорение на 2 ядрах? Нет — время примерно равно ПОСЛЕДОВАТЕЛЬНОМУ выполнению
# потому что GIL не даёт потокам реально работать параллельно на CPU-bound коде
