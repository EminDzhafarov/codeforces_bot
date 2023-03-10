import os
import threading

def Thread(my_funk):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_funk, args=args, kwargs=kwargs)
        my_thread.start()

    return wrapper

@Thread
def script_1():
    print('Запуск бота')
    os.system("Python3 bot.py")

@Thread
def script_2():
    print('Запуск парсера')
    os.system("Python3 parser.py")

t = threading.Thread(target=script_1)
t2 = threading.Thread(target=script_2)

t.start()
t2.start()