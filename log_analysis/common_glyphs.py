#!/usr/bin/env python3

import collections

total_counter = collections.Counter()
character_sets = []

try:
    while True:
        line = input()
        if not line:
            break
        selected = [c for c in line if ord(c) > 1000]
        counter = collections.Counter(selected)
        total_counter.update(selected)
        print(counter.most_common(10))
        character_sets.append(set(selected))

except EOFError:
    pass

print('Total top ten: {0}'.format(total_counter.most_common(10)))

print('Reduced: ', set.intersection(*character_sets))
