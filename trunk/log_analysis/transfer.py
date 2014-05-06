#!/usr/bin/env python

import re
import sys

paths = {}

for line in sys.stdin.readlines():
    path = re.search("GET ([^ ]+) HTTP", line).group(1)
    try:
        size = re.search('200 (\d+) ', line).group(1)
    except:
        raise
        # continue
    if path in paths:
        paths[path]['total'] += int(size)
        paths[path]['count'] += 1
    else:
        paths[path] = {'count': 1, 'total': int(size)}

for total, num, path in sorted((paths[path]['total'], paths[path]['count'], path) for path in paths):
    print "{0}: {1} bytes x {2} times, {3} total.".format(path, total / num, num, total)

