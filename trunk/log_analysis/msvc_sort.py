#!/usr/bin/env python

from collections import defaultdict

import re
import sys

projects = defaultdict(list)
epilogue = []

for line in sys.stdin.readlines():
    m = re.match('(\d+)>', line)
    if m:
        projects[m.group(1)].append(line)
    else:
        epilogue.append(line)

for num in sorted(projects.keys(), key=int):
    sys.stdout.write(''.join(projects[num])+'\n')
sys.stdout.write(''.join(epilogue))
