#!/usr/bin/env python3

import collections

total_counter = collections.Counter()

try:
    while True:
        line = input()
        if not line:
            break
        counter = collections.Counter(c for c in line if ord(c) > 1000)
        total_counter.update(c for c in line if ord(c) > 1000)
        print(counter.most_common(10))
except EOFError:
    pass

print('Total top ten: {0}'.format(total_counter.most_common(10)))
