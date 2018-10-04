# Multi-core processing in Python with Numpy

http://tbnorth.github.io/multiproc



## CPU Loading

![CPU Loading](img/cpu.png)


## threading / multiprocessing / asyncio

- `threading` allows code to keep running while waiting for
  file / network / DB input / output
- `asyncio` ~= better `threading`<br/>(new in Python 3.4)
- `multiprocessing` runs separate processes on separate CPU
  cores


## Cheap, disposable, or expensive, persistent

- Using `threading`, you might cheaply invoke a *function* which
  saves data to disk while the main program runs uninterrupted,
  the thread is used once.
- Using `multiprocessing` start-up cost of the new process will
  exceed savings for trivial operations, but you
  can re-use the process, coordinating with special
  message passing methods.


## Cheap, disposable, or expensive, persistent

- For really long CPU intensive processes `multiprocessing` start-up
  cost may be low enough to allow single use processes


## Summary

- IO bound operations, use `threading`
- small CPU bound operations (< 1-5 sec.), *re-use* processes
  with `multiprocessing` and communication
- large CPU bound operations, like processing a folder of
  images, process reuse doesn't matter


## multiprocessing / NumPy

- `multiprocessing` uses separate instances of “python.exe”
  which can communicate with **expensive** message passing
  to move information between processes
- NumPy supports shared memory for its arrays, so separate
  programs can operate on the same data



## Multi-process / main

```python
from multiprocessing import Process
import os

def hello(n):
    print("Sub-process %s: %s" % (n, os.getpid()))

if __name__ == '__main__':
    for i in range(4):
        proc = Process(target=hello, args=(i,))
        proc.start()
    print("Main process: %s" % os.getpid())
```


## Multi-process / main

```
Sub-process 0: 17409
Sub-process 1: 17410
Main process: 17408
Sub-process 2: 17411
Sub-process 3: 17412
```



## End


