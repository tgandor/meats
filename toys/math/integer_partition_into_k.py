#!/usr/bin/env python

from __future__ import print_function

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('n', type=int, help='the number to "distribute"', nargs='?', default=4)
parser.add_argument('k', type=int, help='number of summands (array size)', nargs='?', default=3)


def first_non_zero(t):
    return next(i for i, x in enumerate(t) if x)

def next_partition(t):
    """Produce next partition in revesed lexicographical order (from the left)."""
    if t[0] != 0:
        t[0] -= 1
        t[1] += 1
        return True

    idx = first_non_zero(t)
    if idx == len(t) - 1:
        t[0], t[idx] = t[idx], t[0]
        return False

    t[idx+1] += 1
    t[0] = t[idx] - 1
    t[idx] = 0
    return True


def partitions(n, k):
    t = [n] + [0] * (k-1)
    yield t
    while next_partition(t):
        yield t


def main():
    args = parser.parse_args()

    for i, t in enumerate(partitions(args.n, args.k)):
        print(i, ':', t[::-1])


if __name__ == '__main__':
    main()
