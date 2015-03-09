#/usr/bin/env python

import sys

print 'digraph {'
for line in sys.stdin.readlines():
    chunks = line.split()
    if len(chunks) == 1:
        print '  ' + line + ';'
    elif len(chunks) == 2:
        print '  {0} -> {1};'.format(chunks[0], chunks[1])
    elif len(chunks) > 0:
        print '  %s -> {%s};' % (chunks[0], ' '.join(chunks[1:]))
print '}'
