import threading
import subprocess

def script_bot():
    """Запускаем телеграм-бот"""
    subprocess.call(["Python3", "bot.py"])

def script_parser():
    """Запускаем парсер"""
    subprocess.call(["Python3", "parser.py"])

t1 = threading.Thread(target=script_bot)
t2 = threading.Thread(target=script_parser)

t1.start()
t2.start()

t1.join()
t2.join()

