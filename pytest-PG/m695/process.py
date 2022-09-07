import multiprocessing
import time
import os

def fun1(num):
    print('1进程PID', os.getpid())
    print('1进程父进程编号', os.getppid())
    for i in range(num):
        print('1....\n')
        time.sleep(0.5)


def fun2(num):
    print('2进程PID', os.getpid())
    print('2进程父进程编号', os.getppid())
    for i in range(num):
        print('2...')
        time.sleep(0.5)

# 1. 导入进程包

if __name__ == '__main__':
    sing_process = multiprocessing.Process(target=fun1, args=(5,))
    dance_process = multiprocessing.Process(target=fun2, kwargs={'num':2}) # target

    #3. 启动进程
    sing_process.start()
    dance_process.start()
