"""Record array allocation sizes and resident memory without exhausting the host."""
import argparse
import gc
import json
import platform
import sys

import numpy as np
import psutil


def demonstrate(elements):
    process = psutil.Process()
    records = []

    def snapshot(command, arrays):
        memory = psutil.virtual_memory()
        try:
            swap_used = psutil.swap_memory().used
            swap_error = None
        except (OSError, PermissionError) as error:
            swap_used = None
            swap_error = f'{type(error).__name__}: swap information is unavailable'
        records.append({'command': command, 'elements': elements,
                        'live_array_bytes': sum(array.nbytes for array in arrays),
                        'process_rss_bytes': process.memory_info().rss,
                        'system_available_bytes': memory.available,
                        'system_swap_used_bytes': swap_used,
                        'swap_measurement_error': swap_error})

    snapshot('import numpy as np', [])
    my_array = np.zeros(elements)
    snapshot('my_array = np.zeros(elements)', [my_array])
    my_array1 = my_array + 1
    snapshot('my_array1 = my_array + 1', [my_array, my_array1])
    my_array2 = my_array + 2
    snapshot('my_array2 = my_array + 2', [my_array, my_array1, my_array2])
    my_array3 = my_array + 3
    snapshot('my_array3 = my_array + 3', [my_array, my_array1, my_array2, my_array3])
    del my_array3
    gc.collect()
    snapshot('del my_array3', [my_array, my_array1, my_array2])
    del my_array1
    gc.collect()
    snapshot('del my_array1', [my_array, my_array2])
    return {'platform': platform.platform(), 'python': sys.version,
            'numpy': np.__version__, 'records': records}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--elements', type=int, default=1_000_000)
    args = parser.parse_args()
    if args.elements <= 0:
        parser.error('--elements must be positive')
    print(json.dumps(demonstrate(args.elements), indent=2))
