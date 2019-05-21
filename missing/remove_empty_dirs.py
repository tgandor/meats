#!/usr/bin/env python

print('Under construction')
exit()

from __future__ import print_function

from collections import defaultdict
import os

exclusions = ['.git']

filesystem = {}

for path, subdirs, files in os.walk('.'):
    print(path, len(subdirs), len(files))
