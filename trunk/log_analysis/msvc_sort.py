#!/usr/bin/env python

from collections import defaultdict

import re
import sys

projects = defaultdict(list)
epilogue = []

input_data = sys.stdin.readlines()
for line in input_data:
    m = re.match('(\d+)>', line)
    if m:
        projects[m.group(1)].append(line)
    else:
        epilogue.append(line)

try:
    eol = re.search('\s+$', input_data[0]).group()
except:
    eol = '\n'

for num in sorted(projects.keys(), key=int):
    sys.stdout.write(''.join(projects[num])+eol)
sys.stdout.write(''.join(epilogue))
