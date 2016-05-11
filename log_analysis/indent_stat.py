#!/usr/bin/env python

import sys
import glob


def analyze(filename):
    tabs = spaces = none = 0
    for line in open(filename):
        if line.startswith(' '):
            spaces += 1
        elif line.startswith('\t'):
            tabs += 1
        else:
            none += 1
    return tabs, spaces, none


def stats(tabs, spaces, none):
    total = tabs + spaces + none
    return 'tabs {} ({}%), spaces {} ({}%), none {} ({}%)'.format(
        tabs, tabs * 100 / total,
        spaces, spaces * 100 / total,
        none, none * 100 / total,
    )


total_stats = [0] * 3


for pattern in sys.argv[1:]:
    for filename in glob.glob(pattern):
        file_stats = analyze(filename)
        print('{}: {}'.format(filename, stats(*file_stats)))
        total_stats = [a + b for a, b in zip(total_stats, file_stats)]


print('Total: {}'.format(stats(*total_stats)))
