#!/usr/bin/env python

import os
import sys

search = sys.argv[1]
replace = sys.argv[2]

for f in sys.argv[3:]:
    target = f.replace(search, replace)
    if f == target:
        print ('File: {0} - not affected.'.format(f))
        continue
    if not os.path.exists(target):
        print ('Moving: {0} -> {1}'.format(f, target))
        os.rename(f, target)
    else:
        print ('Error! File exists: {0}'.format(target))

