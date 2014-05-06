#!/usr/bin/env python

import re
import sys


def human(x):
    for suffix in ['', 'K', 'M', 'G', 'T']:
        if x < 1024:
            return "%.2f %s" % (x, suffix) if x - int(x) > 0.001 else "%d %s" % (int(x), suffix)
        x /= 1024.0
    return "%.1f P" % x

paths = {}

for line in sys.stdin.readlines():
    try:
        path = re.search("GET ([^ ]+) HTTP", line).group(1)
    except AttributeError:
        continue

    try:
        size = re.search('200 (\d+) ', line).group(1)
    except AttributeError:
        continue

    if path in paths:
        paths[path]['total'] += int(size)
        paths[path]['count'] += 1
    else:
        paths[path] = {'count': 1, 'total': int(size)}

for total, num, path in sorted((paths[path]['total'], paths[path]['count'], path) for path in paths):
    print "{3}B : {0} : {1} bytes x {2} times.".format(path, total / num, num, human(total))

