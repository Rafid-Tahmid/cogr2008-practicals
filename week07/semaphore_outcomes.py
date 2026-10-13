"""Enumerate all reachable instruction interleavings, including blocked states."""
import json

PROGRAMS = {
    'a': (['down(m)', 'z=x', 'z++', 'x=z', 'up(m)'],
          ['down(m)', 'y++', 'x=y', 'up(m)']),
    'b': (['down(ml)', 'z=x', 'z++', 'x=z', 'up(m)'],
          ['down(m)', 'y++', 'x=y', 'up(ml)']),
    'c': (['up(ml)', 'z=x', 'z++', 'x=z', 'down(m)'],
          ['up(ml)', 'y++', 'x=y', 'down(ml)']),
    'd': (['down(mx)', 'down(m)', 'z=x', 'z++', 'x=z', 'up(mx)', 'up(m)'],
          ['down(m)', 'down(mx)', 'y++', 'x=y', 'up(m)', 'up(mx)'])
}


def explore(programs):
    seen = set()
    completed = {}
    deadlock = None

    def visit(pc, values, trace):
        nonlocal deadlock
        key = (pc, tuple(values[name] for name in ('x', 'y', 'z', 'm', 'ml', 'mx')))
        if key in seen:
            return
        seen.add(key)
        if all(pc[i] == len(programs[i]) for i in (0, 1)):
            completed.setdefault(values['x'], trace)
            return
        progressed = False
        for proc in (0, 1):
            if pc[proc] == len(programs[proc]):
                continue
            instruction = programs[proc][pc[proc]]
            updated = values.copy()
            if instruction.startswith('down('):
                semaphore = instruction[5:-1]
                if updated[semaphore] == 0:
                    continue
                updated[semaphore] -= 1
            elif instruction.startswith('up('):
                updated[instruction[3:-1]] += 1
            elif instruction == 'z=x':
                updated['z'] = updated['x']
            elif instruction == 'z++':
                updated['z'] += 1
            elif instruction == 'y++':
                updated['y'] += 1
            elif instruction == 'x=z':
                updated['x'] = updated['z']
            elif instruction == 'x=y':
                updated['x'] = updated['y']
            else:
                raise ValueError(instruction)
            next_pc = list(pc)
            next_pc[proc] += 1
            progressed = True
            visit(tuple(next_pc), updated, trace + [f'P{proc + 1}: {instruction}'])
        if not progressed and deadlock is None:
            deadlock = {'values': values, 'trace': trace,
                        'blocked_next': [programs[i][pc[i]] for i in (0, 1)
                                         if pc[i] < len(programs[i])]}

    visit((0, 0), {'x': 0, 'y': 23, 'z': 0, 'm': 1, 'ml': 0, 'mx': 1}, [])
    return {'final_x': sorted(completed), 'example_traces': completed,
            'deadlock': deadlock, 'reachable_states': len(seen)}


if __name__ == '__main__':
    print(json.dumps({name: explore(code) for name, code in PROGRAMS.items()}, indent=2))
