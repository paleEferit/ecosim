import os
import time


def clear_screen():
    msg = ''
    if os.name == 'nt':
        msg = 'cls'
    else:
        msg = 'cleat'
    os.system(msg)

print('Hello world')
clear_screen()
time.sleep(10)
print('Post hello world')
