#!/usr/bin/env python

import os
import re
import sys

testmode = False
if sys.argv[1] == '--test':
    testmode = True
    sys.argv.pop(1)

search = re.compile(sys.argv[1])
replace = sys.argv[2]

for f in sys.argv[3:]:
    target = search.sub(replace, f)
    if f == target:
        print ('File: {0} - not affected.'.format(f))
        continue
    if not os.path.exists(target):
        if testmode:
            print ('Would move: {0} -> {1}'.format(f, target))
        else:
            print ('Moving: {0} -> {1}'.format(f, target))
            os.rename(f, target)
    else:
        print ('Error! File exists: {0}'.format(target))

