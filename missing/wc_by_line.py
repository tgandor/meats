#!/usr/bin/env python

import sys

lines = words = bytes_ = 0

while True:
    line = sys.stdin.readline()
    if line == '':
        break
    lines += 1
    words += len(line.split())
    bytes_ += len(line)
    sys.stdout.write('{0:4} {1:6} {2:8} | {3}'.format(lines, words, bytes_, line))
