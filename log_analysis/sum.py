#!/usr/bin/env python3
# yes, it has come to this

from __future__ import print_function

'''
Filter to sum columns in standard input and append after echoing.
Or better, print to stderr.
'''

import collections
import sys

sums = collections.defaultdict(int)

for line in sys.stdin:
    sys.stdout.write(line)
    for i, field in enumerate(line.split()):
        try:
            sums[i] += int(field)
        except:
            pass

sys.stdout.flush()

print('-' * 20, file=sys.stderr)
print('Totals:', file=sys.stderr)
print('\t'.join('[{}]: {}'.format(k, sums[k]) for k in sorted(sums.keys())), file=sys.stderr)

