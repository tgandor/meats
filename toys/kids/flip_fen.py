#!/usr/bin/env python

import sys

while True:
    line = sys.stdin.readline().split()
    if not line:
        break
    line[0] = '/'.join(line[0].split('/')[::-1])
    print(' '.join(line))

    