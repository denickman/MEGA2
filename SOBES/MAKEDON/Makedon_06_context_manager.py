


# simple
'''
Тут главная проблема: если file.read() упадёт с исключением (например, файл повреждён, или ошибка кодировки) —
строка file.close() никогда не выполнится, потому что исключение прервёт выполнение до неё.
Файл останется открытым навсегда (точнее, пока его не закроет сборщик мусора или ОС — а это ненадёжно).
Это называется утечка ресурса (resource leak).
'''

file = open('data.txt','r')
print(file.read())
file.close()


# better
'''
он многословный: надо не забыть try/finally, не забыть close(), и если забудешь — никакой ошибки Python тебе не покажет,
 просто тихая утечка ресурса.
'''
file = open('data.txt', 'r')
try:
    print(file.read())
finally:
    file.close()


'''
with — это синтаксический сахар, который под капотом делает ровно то же самое, что способ 2 (try/finally), 
но автоматически. Объект, который возвращает open(...), реализует протокол контекстного менеджера — 
у него есть методы __enter__ (вызывается при входе в with, возвращает сам файл, который присваивается f) и __exit__ 
(вызывается при выходе из блока, где как раз и происходит close() — причём __exit__ вызовется даже если внутри блока было исключение)




Как и почему вызываются именно __enter__/__exit__

Это не магия, а чётко определённый протокол контекстного менеджера в Python: любой объект, 
у которого есть методы с именно такими именами (__enter__ и __exit__), автоматически годится для использования с 
оператором with. Python при встрече конструкции with жёстко прописанным образом (это часть синтаксиса языка, 
реализовано в самом интерпретаторе) делает следующее:


with EXPR as VAR:
    BODY
    
    
    
    
'''

# best
with open('data.txt','r') as f:
    print(f.read())


# custom context manager

class FileOpener:
    def __init__(self, path: str, mode: str = 'r'):
        self.path = path
        self.mode = mode

    def __enter__(self):
        self.file = open(self.path, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        print(f'--Error inside {exc_type}, text: {exc_val}')
        return False





with FileOpener('data.txt', 'r') as file:
    print(file.read())




























