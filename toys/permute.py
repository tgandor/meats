#!/usr/bin/env python

import sys
import itertools

for p in itertools.permutations(sys.argv[1]):
    print ''.join(p)

