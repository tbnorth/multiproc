import time
from multiprocessing import Process, JoinableQueue
from queue import Empty


def proc_queue(queue):
    while True:
        try:
            task = queue.get(timeout=5)
        except Empty:
            break
        do_task(task)
        queue.task_done()
    print("(sub-process ends)")


def print_number(n):
    print(n)
    time.sleep(3)


def do_task(task):
    if task['task'] == 'print_number':
        print_number(task['data']['n'])
    else:
        raise Exception("Unknown task: " + task['task'])


if __name__ == '__main__':

    queue = JoinableQueue()

    for i in range(4):
        proc = Process(target=proc_queue, args=(queue,))
        proc.start()

    for i in range(10):
        queue.put({'task': 'print_number', 'data': {'n': i}})

    queue.join()
    print("(main process ends)")
