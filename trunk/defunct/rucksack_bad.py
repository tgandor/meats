#!/usr/bin/env python
import sys

if len(sys.argv) < 3:
    print sys.argv, 'Usage: %s limit item1 ... itemN' % sys.argv[0]
    exit()

limit = float(sys.argv[1])
items = sorted(set(map(float, sys.argv[2:])))

sums = {0: [[]]}
surpassed = set()

# print limit, items

for item in items:
    for i in xrange(1, int(limit/item) + 1):
        for s in sums.keys()[:]:
            if item*i+s <= limit:
                surpassed.add(s)
                if item*i+s not in sums:
                    sums[item*i+s] = [variant+[(item,i)] for variant in sums[s]]
                else:
                    sums[item*i+s].extend(variant+[(item,i)] for variant in sums[s])

for k in sorted(sums.keys(), reverse=True):
    if k not in surpassed:
        print k
        for n, s in sorted( ((sum(xx[1] for xx in x), x) for x in sums[k]),
        reverse = True):
            print n, s

