#!/usr/bin/env python

import sys

forks = [open(f, 'wb') for f in sys.argv[1:]]

while True:
    line = sys.stdin.readline()
    if not line:
        break
    sys.stdout.write(line)
    sys.stdout.flush()
    for f in forks:
        f.write(line)

for f in forks:
    f.close()

