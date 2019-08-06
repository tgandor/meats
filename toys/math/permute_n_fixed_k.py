#!/usr/bin/env python

# this is for benchmarking, above 9 starts to take forever.

# https://oeis.org/A008290
# Triangle T(n, k) of rencontres numbers (number of permutations of n elements with k fixed points).

from __future__ import print_function
from collections import Counter
from itertools import permutations
import argparse
import sys


def factorial(n):
    res = 1
    for k in range(2, n):
        res *= k
    return res


def num_fixed(p):
    return sum(i == x for i, x in enumerate(p))


def permute_fixed_counts(n):
    c = Counter()

    for p in permutations(range(n)):
        c[num_fixed(p)] += 1

    return c


parser = argparse.ArgumentParser()
parser.add_argument('--mod', type=int)
parser.add_argument('max_n', type=int, default=10, nargs='?')
args = parser.parse_args()

max_n = args.max_n

print(' 0 : 1')  # for 0 - by definition

for n in range(1, max_n):
    stats = permute_fixed_counts(n)

    print('{:2}'.format(n), ':', end=' ')
    if args.mod:
        for k in range(n):
            print(stats[k] % args.mod, end=',')
    else:
        for k in range(n):
            print(stats[k], end=',')

    print(stats[n])
    sys.stdout.flush()

