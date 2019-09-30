from __future__ import print_function, division

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('max_elements', nargs='?', default=1000, type=int, help='dict size limit')
parser.add_argument(
    '--incremental', '-i', action='store_true',
    help='reuse 1 dict, recommended for large N'
)
args = parser.parse_args()

d = dict()
prev = sys.getsizeof(d)
print(0, prev)

for i in range(1, args.max_elements):
    if args.incremental:
        d[i] = i
    else:
        d = dict(zip(range(i), range(i)))

    val = sys.getsizeof(d)

    if val != prev:
        print(i, val, '\tB/item: {:.1f}'.format(val / i))
        prev = val
