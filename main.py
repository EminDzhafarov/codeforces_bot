import threading
import subprocess

def script1():
    subprocess.call(["Python3", "bot.py"])

def script2():
    subprocess.call(["Python3", "parser.py"])

t1 = threading.Thread(target=script1)
t2 = threading.Thread(target=script2)

t1.start()
t2.start()

t1.join()
t2.join()

