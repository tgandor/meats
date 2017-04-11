#!/usr/bin/env python

import sys

force = len(sys.argv) > 1 and sys.argv[1] == '2'
labels = len(sys.argv) > 1 and sys.argv[1] == 'L'

print('graph {')
for line in sys.stdin.readlines():
    chunks = line.split()
    if len(chunks) == 0:
        continue
    elif len(chunks) == 1:
        print('  ' + line + ';')
    elif len(chunks) == 2 or force:
        print('  {0} -- {1};'.format(*chunks[:2]))
    elif len(chunks) == 3 and labels:
        print('  {0} -- {1} [label="{2}"];'.format(*chunks))
    elif len(chunks) > 0:
        print('  %s -- {%s};' % (chunks[0], ' '.join(chunks[1:])))
print('}')
