import numpy as np
import time
from multiprocessing import Array, JoinableQueue, Process


def setup(queue, shared_grid, rows, cols):
    global grid
    grid = np.frombuffer(shared_grid)
    grid.shape = (rows, cols)
    proc_queue(queue)


def proc_queue(queue):
    while True:
        task = queue.get()
        if task['task'] == 'exit':
            break
        do_task(task)
        queue.task_done()
    print("(sub-process ends)")


def inc_rows(start, end):
    print("Doing %s-%s" % (start, end))
    for row in range(start, end):
        for col in range(grid.shape[1]):
            for i in range(1000000):
                grid[row][col] += 0.000001 * col + row


def do_task(task):
    if task['task'] == 'inc_rows':
        inc_rows(task['data']['start'], task['data']['end'])
    else:
        raise Exception("Unknown task: " + task['task'])


if __name__ == '__main__':

    queue = JoinableQueue()

    rows, cols = 10, 10

    shared_grid = Array('d', rows * cols, lock=False)
    grid = np.frombuffer(shared_grid)
    grid.shape = (rows, cols)

    for i in range(2):
        proc = Process(target=setup, args=(queue, shared_grid, rows, cols))
        proc.start()

    start = time.time()
    for i in range(4):
        queue.put(
            {'task': 'inc_rows', 'data': {'start': 3 * i, 'end': min(rows, 3 * i + 3)}}
        )
    queue.join()
    print("done in %s" % (time.time() - start))
    answer0 = np.array(grid)
    grid[:] = 0
    start = time.time()
    queue.put({'task': 'inc_rows', 'data': {'start': 0, 'end': 10}})
    queue.join()
    print("done in %s" % (time.time() - start))
    answer1 = np.array(grid)

    assert (answer0 == answer1).all()

    for i in range(2):
        queue.put({'task': 'exit'})
