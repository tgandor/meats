#!/usr/bin/env python

import matplotlib.pyplot as plt
import sys

x = []
y = []

for line in sys.stdin.readlines():
    chunks = line.split()[:2]
    if len(chunks) < 2:
        continue
    xi, yi = map(float, chunks)
    x.append(xi)
    y.append(yi)

plt.scatter(x, y)
for i in xrange(len(x)):
    plt.annotate(str(i), xy=(x[i], y[i]), xytext=(x[i]-0.3, y[i]-0.3))
plt.show()
