#!/usr/bin/env python3

import argparse
import threading
import os
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty
import shutil
import time

KB = 2**10
MB = 2**20

# configuration
check_interval = 5 # s
log_threshold = 10 * MB

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--log', default='df_log.csv')
parser.add_argument('--min-change', type=int, default=log_threshold)
parser.add_argument('paths', type=str, nargs='+')


def get_usage(paths):
    # todo: py2
    return [shutil.disk_usage(p) for p in paths]


def print_header(f, paths):
    headers = ['Timestamp']
    for p in paths:
        headers.append('')
        headers.append('Used ' + p)
        headers.append('Free ' + p)
    headers.append('')
    headers.append('Comment')
    f.write(','.join(headers)+'\n')


def print_data(f, comment, current, previous, initial):
    data = [time.strftime('%Y-%m-%d %H:%M:%S')]
    for c, _, _ in zip(current, previous, initial):
        data.append('')
        data.append(str(c.used))
        data.append(str(c.free))
    data.append('')
    data.append(comment)
    f.write(','.join(data)+'\n')
    print(', '.join(data))


def log_disk_usage():
    previous = initial = get_usage(args.paths)
    comment_queue = Queue()
    comment_reader = threading.Thread(target=read_comments, args=(comment_queue,))
    comment_reader.start()
    append = os.path.exists(args.log)
    with open(args.log, 'a' if append else 'w') as f:
        print_header(f, args.paths)
        print_data(f, 'starting df_log.py', initial, previous, initial)

        while True:
            try:
                comment = comment_queue.get(True, timeout=check_interval)
            except Empty:
                comment = ''

            current = get_usage(args.paths)

            total_change = sum(abs(p.used - c.used) for p, c in zip(previous, current))

            if total_change < args.min_change and not comment:
                continue

            print_data(f, comment, current, previous, initial)
            previous = current

            if comment in ['quit', 'exit']:
                break


def read_comments(q):
    while True:
        line = input('Enter comment:')
        q.put(line)
        if line in ['quit', 'exit']:
            break


if __name__ == '__main__':
    args = parser.parse_args()
    log_disk_usage()
