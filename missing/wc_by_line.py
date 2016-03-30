#!/usr/bin/env python

import sys

lines = words = bytes_ = 0

infile = next(iter(sys.argv[1:]), None)
input_ = open(infile) if infile else sys.stdin

while True:
    line = input_.readline()
    if line == '':
        break
    lines += 1
    words += len(line.split())
    bytes_ += len(line)
    sys.stdout.write('{0:4} {1:6} {2:8} | {3}'.format(lines, words, bytes_, line))
