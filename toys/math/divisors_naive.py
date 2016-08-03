#!/usr/bin/env python

import sys

n = int(sys.argv[1])

i = 2
while i <= n/2:
    if n % i == 0:
        print("{} (x {})".format(i, n//i))
    i += 1
