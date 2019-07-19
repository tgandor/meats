#!/usr/bin/env python

from __future__ import print_function

import argparse

import numpy as np


def levenshtein(a, b):
    n, m = len(a), len(b)
    dist = np.empty((n+1, m+1), dtype=np.int)
    dist[0, :] = np.arange(m+1)
    dist[:, 0] = np.arange(n+1)
    for i in range(n):
        for j in range(m):
            cost = 0 if a[i] == b[j] else 1
            dist[i+1, j+1] = min(
                dist[i+1, j] + 1,
                dist[i, j+1] + 1,
                dist[i, j] + cost
            )
    return dist


def explain(a, b, d):
    i, j = len(a), len(b)
    print('explaining', a, '->', b)
    actions = []
    costs = []
    while i > 0 and j > 0:
        cost = 1
        # prioritize going diagonally!
        # other solutions may generate excess cost
        min_i, min_j = i-1, j-1
        if a[i-1] == b[j-1]:
            cost = 0
            action = 'keep {} at position {}'.format(a[i-1], j)
        else:
            action = 'replace {} with {} at position {}'.format(a[i-1], b[j-1], j)
        if d[i-1, j] < d[min_i, min_j]:
            min_i, min_j = i-1, j
            action = 'delete {} at position {}'.format(a[i-1], i)
        if d[i, j-1] < d[min_i, min_j]:
            min_i, min_j = i, j-1
            action = 'insert {} at position {}'.format(b[j-1], j)
        if d[i-1, j-1] < d[min_i, min_j]:
            min_i, min_j = i-1, j-1
            if a[i-1] == b[j-1]:
                cost = 0
                action = 'keep {} at position {}'.format(a[i-1], j)
            else:
                action = 'replace {} with {} at position {}'.format(a[i-1], b[j-1], j)
        i, j = min_i, min_j
        actions.append(action)
        costs.append(cost)

    if j > 0:
        actions.append('insert (type) "{}" at the beginning'.format(b[:j]))
        costs.append(j)
    if i > 0:
        actions.append('skip initial "{}"'.format(a[:i]))
        costs.append(i)

    costs = costs[::-1]
    total = 0

    for i, action in enumerate(reversed(actions)):
        total += costs[i]
        print(i+1, ':', action)
        print('\tcost:', costs[i], 'total:', total, sep='\t')


parser = argparse.ArgumentParser()
parser.add_argument('word1')
parser.add_argument('word2')
parser.add_argument('--verbose', '-v', action='store_true')
args = parser.parse_args()

d = levenshtein(args.word1, args.word2)
if args.verbose:
    print(d)
    explain(args.word1, args.word2, d)
else:
    print(d[-1, -1])
