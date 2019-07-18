#!/usr/bin/env python

"""
Generating weak integer compositions of a number (N),
having a fixed size (K).

If you need strong compositions of size K, you can add
np.ones(k) to every of the weak_compositions(n-k, k).

Not to be confused with a related concept - integer partitions (subsets).

Bibliography:
1. Integer partitions:
https://stackoverflow.com/questions/10035752/elegant-python-code-for-integer-partitioning
http://jeromekelleher.net/generating-integer-partitions.html
https://arxiv.org/abs/0909.2331
Older algo: https://pdfs.semanticscholar.org/9613/c1666b5e48a5035141c8927ade99a9de450e.pdf
- the fastest method for it is related to integer compositions, albeit only ascending ones.

2. https://en.wikipedia.org/wiki/Composition_(combinatorics)
- this is analogous to a 2 ** (n-1), where n-1 is the number of possible "joints" between ones.
"""

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


def weak_compositions(n, k):
    t = [n] + [0] * (k-1)
    yield t
    while next_partition(t):
        yield t


def main():
    args = parser.parse_args()

    for i, t in enumerate(weak_compositions(args.n, args.k)):
        print(i, ':', t[::-1])


if __name__ == '__main__':
    main()
