#!/usr/bin/env python

from __future__ import print_function

import re
import sys

for line in sys.stdin:
    line = line[::-1]
    line, _ = re.subn(r'(\d{3})(?=\d+\s|\d+$)', r'\1,', line)
    print(line[::-1], end='')
