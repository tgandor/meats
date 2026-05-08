#!/usr/bin/env python

import os
import sys

for line in sys.stdin:
    line = line.rstrip()
    line = line.replace(os.getcwd(), '.')
    print(line)
