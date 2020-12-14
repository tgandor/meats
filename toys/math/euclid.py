#!/usr/bin/env python

# euclid algorithm in steps
# letters: m, n - like in AoCP 1.1

import sys

m, n = map(int, sys.argv[1:])

while True:
    r = m % n
    print('rest', r)
    if r == 0:
        break
    m, n = n, r

print('Result:', n)
