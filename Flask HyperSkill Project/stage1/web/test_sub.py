import subprocess
import threading
from time import sleep

process = None


def start_program():
    global process
    process = subprocess.run('python main.py', shell=True)
    print(process)


th = threading.Thread(target=start_program)
th.start()
sleep(2)
