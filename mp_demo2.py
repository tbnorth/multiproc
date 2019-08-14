"""Demo multiprocessing a NumPy shared memory array"""

import numpy as np
import time
from multiprocessing import Array, JoinableQueue, Process


def setup(queue, shared_grid, rows, cols):
    """make NumPy array from shared array and start watching queue"""
    global grid
    grid = np.frombuffer(shared_grid)
    grid.shape = (rows, cols)
    proc_queue(queue)


def proc_queue(queue):
    """process tasks from queue until an exit task is seen"""
    while True:
        task = queue.get()
        if task['task'] == 'exit':
            break
        do_task(task)
        queue.task_done()
    print("(sub-process ends)")


def inc_rows(start, end):
    """process rows start...end in shared array"""
    print("Doing %s-%s" % (start, end))
    for row in range(start, end):
        for col in range(grid.shape[1]):
            for i in range(1000000):
                grid[row][col] += 0.000001 * col + row


def do_task(task):
    """direct a task to the appropriate function"""
    if task['task'] == 'inc_rows':
        inc_rows(task['data']['start'], task['data']['end'])
    else:
        raise Exception("Unknown task: " + task['task'])


if __name__ == '__main__':

    queue = JoinableQueue()

    rows, cols = 10, 10

    # create shared array
    shared_grid = Array('d', rows * cols, lock=False)
    # and regular NumPy array using shared array memory
    grid = np.frombuffer(shared_grid)
    grid.shape = (rows, cols)

    for i in range(2):
        proc = Process(target=setup,
            args=(queue, shared_grid, rows, cols))
        proc.start()

    start = time.time()
    for i in range(4):
        queue.put({
            'task': 'inc_rows',
            'data': {
                 'start': 3 * i,
                 'end': min(rows, 3 * i + 3)
            }
        })
    queue.join()
    print("done in %s" % (time.time() - start))
    answer0 = np.array(grid)  # copy answer for comparison later

    # end of first run, redo with one process to compare time

    grid[:] = 0  # zero out grid again
    start = time.time()
    queue.put({
        'task': 'inc_rows',
        'data': {'start': 0, 'end': 10}
    })
    queue.join()
    print("done in %s" % (time.time() - start))
    answer1 = np.array(grid)

    assert (answer0 == answer1).all()  # check answers match

    for i in range(2):  # tell both processess to exit
        queue.put({'task': 'exit'})
