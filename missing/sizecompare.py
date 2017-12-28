#!/usr/bin/env python

from __future__ import print_function, division

import os
import sys
import glob

from itertools import groupby
from operator import itemgetter
from collections import namedtuple

info = namedtuple('info', 'file size path')

files = sorted([
    info(os.path.basename(f), os.path.getsize(f), f)
    for subdir in sys.argv[1:]
    for f in glob.glob(os.path.join(subdir, '*'))
])

mins, maxes = 0, 0

for f, group in groupby(files, itemgetter(0)):
    group = list(reversed(list(group)))
    print(f)
    max_size = group[0].size
    print('{:,}'.format(max_size), os.path.dirname(group[0].path))
    for _, size, path in group[1:]:
        print('->',
              '{:,}'.format(size),
              os.path.dirname(path),
              '{:.2f}%'.format(size / max_size * 100),
              '-{:.2f}%'.format(100 - size / max_size * 100),
              '{:.2f}x'.format(max_size / size))
    mins += group[-1].size
    maxes += max_size
    print('---')

print('Summary:',
      '{:,}'.format(maxes),
      '->',
      '{:,}'.format(mins),
      '{:.2f}%'.format(mins / maxes * 100),
      '-{:.2f}%'.format(100 - mins / maxes * 100),
      '{:.2f}x'.format(maxes / mins))
