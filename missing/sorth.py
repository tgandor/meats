#!/usr/bin/env python

import sys
import re

tokener = re.compile('^([0-9.,]+)([KMGT]?)')
scale = {'K': 2**10, 'M': 2**20, 'G': 2**30, 'T': 2**40}

def getBytes(line):
    m = tokener.search(line)
    if m:
        return float(m.group(1).replace(',','.')) * scale[m.group(2)] if len(m.group(2)) else float(m.group(1).replace(',','.'))
    return 0.0

if __name__ == '__main__':
    inlines = sys.stdin.readlines()
    sys.stdout.write("".join(sorted(inlines, key=getBytes)))

