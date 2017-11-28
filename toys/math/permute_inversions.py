#!/usr/bin/env python

from __future__ import print_function

from argparse import ArgumentParser
from itertools import permutations

import numpy as np

parser = ArgumentParser()
parser.add_argument('--table', '-t', action='store_true', help='Calculate and print permutation table')
parser.add_argument('--stable', '-s', action='store_true',
                    help='Only print stable permutations i.e. where inversions == N*(N-1)/4 (half of max)')
parser.add_argument('N', type=int, help='Number of elements in the permutation')
args = parser.parse_args()


def inversions(a):
    """
    Calculate inversions (number of inversely ordered pairs) in an array.
    :param a: a permutation to compute inversions in
    :return: int Number of permutation inversions in array a
    """
    a = np.asanyarray(a)
    return sum(sum(a[:i] > a[i]) for i in range(1, len(a)))


def inversion_table(a):
    a = np.asanyarray(a)
    return [sum(a[:i] > a[i]) for i in range(len(a))]


N = args.N
max_inv = N * (N-1) // 2
# print('Max inversions', max_inv)


for i, p in enumerate(permutations(np.arange(N))):
    inv = inversions(p)

    if 2 * inv != max_inv and args.stable:
        continue

    print(i, p, 'inversions:', inv, end=' ' if args.table else '\n')
    if args.table:
        print('inversion table:', inversion_table(p))
