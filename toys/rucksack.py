#!/usr/bin/env python
import sys

if len(sys.argv) < 3:
    print sys.argv, 'Usage: %s limit item1 ... itemN' % sys.argv[0]
    exit()

limit = float(sys.argv[1])
items = sorted(set(map(float, sys.argv[2:])))

sums = {0: []}
surpassed = set()

for item in items:
    while True:
        changes = False
        for s in sums.keys()[:]:
            if item+s <= limit:
                surpassed.add(s)
                if item+s not in sums:
                    sums[item+s] = sums[s]+[item]
                    changes = True
        if not changes:
            break

for k in sorted(sums.keys(), reverse=True):
    if k not in surpassed:
        print k, sums[k]

