"""Calculate request ordering, seek distance, block transfer time, and inode capacity."""
import json


def main():
    requests = [11, 15, 18, 6, 13, 7, 5, 8]
    pending = requests.copy()
    head = 9
    shortest = []
    while pending:
        request = min(pending, key=lambda value: (abs(value - head), value))
        pending.remove(request)
        shortest.append(request)
        head = request
    above = sorted(value for value in requests if value >= 9)
    below = sorted(value for value in requests if value < 9)
    orders = {'FCFS': requests, 'SSTF': shortest,
              'SCAN': above + below[::-1], 'C-SCAN': above + below}
    distances = {name: sum(abs(right - left) for left, right in
                          zip([9] + order, order)) for name, order in orders.items()}
    pointers = 4096 // 4
    blocks = 10 + pointers + pointers ** 2 + pointers ** 3
    return {'orders': orders, 'head_movement_including_return': distances,
            'rotational_delay_ms': 60 / 6000 * 1000 / 2,
            'average_seek_ms': 5, 'total_block_ms': 6000 / 400,
            'transfer_ms': 5, 'raw_bytes_per_second': 10000 / 0.005,
            'inode_data_blocks': blocks, 'max_file_bytes': blocks * 4096,
            'max_file_TiB': blocks * 4096 / 2 ** 40,
            'block_1200_reads_with_cold_pointer_blocks': 3}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
