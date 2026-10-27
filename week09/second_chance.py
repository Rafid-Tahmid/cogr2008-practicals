"""A small clock/second-chance page replacement implementation."""
import json


class Clock:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError('Frame capacity must be positive')
        self.frames = [None] * capacity
        self.referenced = [False] * capacity
        self.hand = 0

    def access(self, page):
        if page in self.frames:
            self.referenced[self.frames.index(page)] = True
            return False
        while self.frames[self.hand] is not None and self.referenced[self.hand]:
            self.referenced[self.hand] = False
            self.hand = (self.hand + 1) % len(self.frames)
        self.frames[self.hand] = page
        self.referenced[self.hand] = True
        self.hand = (self.hand + 1) % len(self.frames)
        return True


if __name__ == '__main__':
    clock = Clock(3)
    accesses = [1, 2, 3, 1, 4, 2, 5]
    trace = []
    for page in accesses:
        fault = clock.access(page)
        trace.append({'page': page, 'fault': fault, 'frames': clock.frames.copy(),
                      'referenced': clock.referenced.copy(), 'hand': clock.hand})
    print(json.dumps({'faults': sum(row['fault'] for row in trace), 'trace': trace}, indent=2))
