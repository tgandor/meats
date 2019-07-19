#!/usr/bin/env python

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


parser = argparse.ArgumentParser()
parser.add_argument('word1')
parser.add_argument('word2')
parser.add_argument('--verbose', '-v', action='store_true')
args = parser.parse_args()

d = levenshtein(args.word1, args.word2)
if args.verbose:
    print(d)
else:
    print(d[-1, -1])

