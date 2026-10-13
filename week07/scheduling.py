"""Compute the practical's round-robin timeline and ten MLFQ dispatches."""
from collections import deque
import json


def round_robin():
    remaining = {1: 66, 2: 24, 3: 43}
    queue = deque(remaining)
    time = 0
    rows = []
    completed = {}
    while queue:
        task = queue.popleft()
        start = time
        used = min(19, remaining[task])
        remaining[task] -= used
        time += used
        cpu_end = time
        time += 1  # Course convention includes a switch after the final exit.
        rows.append({'task': task, 'start': start, 'cpu_end': cpu_end,
                     'switch_end': time, 'remaining': remaining[task]})
        if remaining[task]:
            queue.append(task)
        else:
            completed[task] = time
    return {'timeline': rows, 'course_completion': completed, 'elapsed': time,
            'switch_percent': len(rows) / time * 100,
            'average_course_completion': sum(completed.values()) / len(completed),
            'without_final_switch': time - 1,
            'actual_cpu_finish': {row['task']: row['cpu_end'] for row in rows
                                  if row['remaining'] == 0}}


def mlfq(iterations=10):
    queues = [deque(['A', 'B', 'C']), deque(), deque()]
    remaining = {'A': 10, 'B': 20, 'C': 10}
    io = []
    time = 0
    rows = []
    for iteration in range(1, iterations + 1):
        for ready, task in sorted(io):
            if ready <= time:
                queues[0].append(task)
        io = [(ready, task) for ready, task in io if ready > time]
        level = next(index for index, queue in enumerate(queues) if queue)
        task = queues[level].popleft()
        quantum = (2, 4, 8)[level]
        used = min(quantum, remaining[task], 1 if task == 'C' else remaining[task])
        start = time
        time += used
        remaining[task] -= used
        # Each iteration is a full dispatch; no mid-quantum I/O preemption.
        for ready, ready_task in sorted(io):
            if ready <= time:
                queues[0].append(ready_task)
        io = [(ready, ready_task) for ready, ready_task in io if ready > time]
        if task == 'C':
            io.append((time + 1, task))
        elif remaining[task]:
            queues[min(level + 1, 2)].append(task)
        rows.append({'iteration': iteration, 'start': start, 'end': time,
                     'ran': task, 'remaining': remaining.copy(),
                     'queues': [list(queue) for queue in queues],
                     'io': [{'ready': ready, 'task': task} for ready, task in io]})
    return rows


if __name__ == '__main__':
    print(json.dumps({'round_robin': round_robin(), 'mlfq_dispatches': mlfq()}, indent=2))
