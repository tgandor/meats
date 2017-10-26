#!/usr/bin/env python

import os

while True:
    line = os.stdin.readline().split()
    line[0] = '/'.join(line[0].split('/')[::-1])
    print(' '.join(line))

    