from multiprocessing import Process
import os

def hello(n):
    print("Sub-process %s: %s" % (n, os.getpid()))

if __name__ == '__main__':
    for i in range(4):
        proc = Process(target=hello, args=(i,))
        proc.start()
    print("Main process: %s" % os.getpid())
