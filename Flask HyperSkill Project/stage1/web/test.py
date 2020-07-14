import os
import threading


def start():
    print(4444)
    os.system('python main.py')


x = threading.Thread(target=start)
x.start()
print(12)

os.system('exit()')
