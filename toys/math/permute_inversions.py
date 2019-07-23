#!/usr/bin/env python

from __future__ import print_function

from argparse import ArgumentParser
from itertools import permutations
from string import ascii_letters

import numpy as np

parser = ArgumentParser()
parser.add_argument('--table', '-t', action='store_true', help='Calculate and print permutation table')

# I don't remember where I got this definition of a "stable permutation", but is is something different than:
# https://www.sciencedirect.com/science/article/pii/0012365X86901214
parser.add_argument('--stable', '-s', action='store_true',
                    help='Only print stable permutations i.e. where inversions == N*(N-1)/4 (half of max)')

parser.add_argument('--no-fixed', '-nf', action='store_true',
                    help='Only print permutations where p(i) != i, i.e. having no cycles of lenght 1')
parser.add_argument('--cycle', '-c', action='store_true', help='Only print 1-cycle permutations. count: (n-1)!')
parser.add_argument('--ascii', '-a', action='store_true', help='Format permutation as letters')
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


def format(p, ascii=False):
    if ascii:
        return ', '.join(ascii_letters[x] for x in p)

    return p


def not_single_cycle(p):
    count = index = 0

    while True:
        index = p[index]
        count += 1
        if index == 0:
            break

    return count != len(p)


N = args.N
max_inv = N * (N-1) // 2
# print('Max inversions', max_inv)


for i, p in enumerate(permutations(np.arange(N))):
    if (args.no_fixed or args.cycle) and any(x == i for i, x in enumerate(p)):
        continue

    if args.cycle and not_single_cycle(p):
        continue

    inv = inversions(p)

    if 2 * inv != max_inv and args.stable:
        continue

    print('%5d' % i, format(p, args.ascii), 'inversions:', inv, end=' ' if args.table else '\n')

    if args.table:
        print('inversion table:', inversion_table(p))
