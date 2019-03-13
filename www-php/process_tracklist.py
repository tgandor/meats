#!/usr/bin/env python

from __future__ import print_function

"""
This may be a useful script for music_index.php
You need a file with lines containing:
<mp3 file basename> <description to put into file.txt>
"""

import glob
import itertools
import os
import sys


def _eager_groupby(iterable, keyfunc=None):
    """Just groupby, but not lazy.
    >>> _eager_groupby(range(10), lambda x: x // 3)
    [(0, [0, 1, 2]), (1, [3, 4, 5]), (2, [6, 7, 8]), (3, [9])]
    >>> _eager_groupby(range(10))
    [(0, [0]), (1, [1]), (2, [2]), (3, [3]), (4, [4]), (5, [5]), (6, [6]), (7, [7]), (8, [8]), (9, [9])]
    """
    return [(key, list(grouper)) for key, grouper in itertools.groupby(iterable, keyfunc)]


def _create_description(filename, description):
    basename, _ = os.path.splitext(filename)

    with open(basename + '.txt', 'w') as f:
        f.write(description + '\n')

    print(basename, '=>', description)


def generate_by_basename_on_first_column(description_filename):
    processed_count = 0
    for line in open(description_filename):
        bnd = line.split(None, 1)
        if len(bnd) != 2:
            continue

        basename, description = bnd
        mp3 = basename + '.mp3'

        if os.path.exists(mp3):
            _create_description(mp3, description)
            processed_count += 1

    return processed_count


def generate_by_unique_prefix(description_filename):
    processed_count = 0
    mp3s = glob.glob('*.mp3')
    descriptions = set(open(description_filename).read().split('\n'))

    if not mp3s or not descriptions:
        print('Missing mp3 files or descriptions')
        return 0

    prefix = 0
    while True:
        prefix += 1
        def key(name):
            return name[:prefix]
        print('Trying prefix', prefix)
        mp3_groups = _eager_groupby(mp3s, key)
        descrption_groups = dict(_eager_groupby(descriptions, key))

        if not all(len(values) == 1 for _, values in mp3_groups):
            print('Not all mp3s unique for prefix', prefix)
            continue

        if not all(len(descrption_groups.get(prefix_key, [])) > 0 for prefix_key, _ in mp3_groups):
            print('ERROR: Not all mp3s have any description for prefix', prefix)
            print([
                (prefix_key, values, descrption_groups.get(prefix_key, []), len(descrption_groups.get(prefix_key, []))) 
                for prefix_key, values in mp3_groups 
                if len(descrption_groups.get(prefix_key, [])) <= 0][:3]
            )
            return 0

        if all(len(descrption_groups[prefix_key]) == 1 for prefix_key, _ in mp3_groups):
            print('SUCCESS: All mp3s have a unique description for prefix', prefix)
            break

    for key, one_mp3 in mp3_groups:
        assert len(one_mp3) == 1
        filename = one_mp3[0]
        description = descrption_groups[key][0]
        _create_description(filename, description)
        processed_count += 1

    return processed_count


if __name__ == '__main__':
    if generate_by_basename_on_first_column(sys.argv[1]) > 0:
        exit()
    print('No file processed normally, trying costly heuristic...')
    generate_by_unique_prefix(sys.argv[1])
