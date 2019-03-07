#!/usr/bin/env python

from __future__ import print_function

"""
This may be a useful script for music_index.php
You need a file with lines containing:
<mp3 file basename> <description to put into file.txt>
"""

import os
import sys

for line in open(sys.argv[1]):
    bnd = line.split(None, 1)
    if len(bnd) != 2:
        continue

    basename, description = bnd

    if os.path.exists(basename + '.mp3'):
        with open(basename + '.txt', 'w') as f:
            f.write(description + '\n')

        print(basename, '=>', description)
