#!/usr/bin/env python

import sys
import glob


def analyze(filename):
    tabs = spaces = none = empty = 0
    for line in open(filename):
        if line.startswith(' '):
            spaces += 1
        elif line.startswith('\t'):
            tabs += 1
        elif line.strip() == '':
            empty += 1
        else:
            none += 1
    return tabs, spaces, none, empty


def stats_all(tabs, spaces, none, empty):
    total = tabs + spaces + none + empty
    return 'tabs {} ({}%), spaces {} ({}%), none {} ({}%), empty {} ({}%)'.format(
        tabs, tabs * 100 / total,
        spaces, spaces * 100 / total,
        none, none * 100 / total,
        empty, empty * 100 / total
    )


def stats_indented(tabs, spaces, none, empty):
    total = tabs + spaces
    return 'tabs {} ({}%), spaces {} ({}%)'.format(
        tabs, tabs * 100 / total,
        spaces, spaces * 100 / total
    )


def stats_nonempty(tabs, spaces, none, empty):
    total = tabs + spaces + none
    return 'tabs {} ({}%), spaces {} ({}%), none {} ({}%)'.format(
        tabs, tabs * 100 / total,
        spaces, spaces * 100 / total,
        none, none * 100 / total
    )


stat_format = stats_nonempty

total_stats = [0] * 4


for pattern in sys.argv[1:]:
    for filename in glob.glob(pattern):
        file_stats = analyze(filename)
        print('{}: {}'.format(filename, stat_format(*file_stats)))
        total_stats = [a + b for a, b in zip(total_stats, file_stats)]


print('Total: {}'.format(stat_format(*total_stats)))
