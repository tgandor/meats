#!/usr/bin/env python

from __future__ import print_function

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('n', type=int, help='the number to partition', nargs='?', default=4)
args = parser.parse_args()

# http://jeromekelleher.net/generating-integer-partitions.html
# https://arxiv.org/abs/0909.2331
# TODO: read article, explain how it works.


def rule_asc(n):
    """Generate integer partitions from Ascending Compositions."""
    a = [0 for i in range(n + 1)]
    k = 1
    a[1] = n
    while k != 0:
        x = a[k - 1] + 1
        y = a[k] - 1
        k -= 1
        while x <= y:
            a[k] = x
            y -= x
            k += 1
        a[k] = x + y
        yield a[:k + 1]


args = parser.parse_args()

for i, t in enumerate(rule_asc(args.n)):
    print(i, ':', t)
