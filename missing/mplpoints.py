#!/usr/bin/env python

import argparse
import sys

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--no-labels', '-n', action='store_true')
args = parser.parse_args()

x = []
y = []

for i, line in enumerate(sys.stdin.readlines()):
    chunks = line.split()[:2]
    if len(chunks) < 1:
        continue

    if len(chunks) == 1:
        xi = i
        yi = float(chunks[0])
    else:
        xi, yi = map(float, chunks)

    x.append(xi)
    y.append(yi)

plt.scatter(x, y)

if not args.no_labels:
    # limit labels to about 100 (by skipping)
    for i in range(0, len(x), len(x) // 100 + 1):
        plt.annotate(str(i), xy=(x[i], y[i]), xytext=(x[i]-0.3, y[i]-0.3))

plt.show()
