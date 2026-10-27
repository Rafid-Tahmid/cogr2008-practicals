"""Compare object identities in separate parent and child address spaces."""
import argparse
import ctypes
import os
import platform
import sys
import time


def demonstrate(start, delay):
    x = start
    before = id(x)
    print(f'Before fork: value={x!r}, object_id={before}', flush=True)
    sys.stdout.flush()
    pid = os.fork()
    if pid == 0:
        x += 2
        print(f'Child: pid={os.getpid()}, parent={os.getppid()}, '
              f'value={x!r}, object_id={id(x)}', flush=True)
        time.sleep(delay)
        os._exit(0)
    x += 1
    print(f'Parent: pid={os.getpid()}, child={pid}, '
          f'value={x!r}, object_id={id(x)}', flush=True)
    time.sleep(delay)
    _, status = os.waitpid(pid, 0)
    if os.waitstatus_to_exitcode(status) != 0:
        raise RuntimeError('The child process failed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--delay', type=float, default=0)
    args = parser.parse_args()
    print(platform.platform(), platform.python_implementation(), sys.version, flush=True)
    x = 10
    y = 10
    print(f'x=10, y=10: id(x)={id(x)}, id(y)={id(y)}', flush=True)
    y += 1
    print(f'After y+=1: x={x}, y={y}, id(x)={id(x)}, id(y)={id(y)}', flush=True)
    print('ctypes retrieval:', ctypes.cast(id(x), ctypes.py_object).value, flush=True)
    demonstrate(10, args.delay)
    demonstrate(10.0, args.delay)
