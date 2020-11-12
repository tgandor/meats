#!/usr/bin/env python

import sys

m, n = map(int, sys.argv[1:])

while True:
    r = m % n
    print('rest', r)
    if r == 0:
        break
    m, n = n, r

print('Result:', n)
