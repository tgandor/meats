#!/usr/bin/env python

import re
import sys
from collections import defaultdict

stats = defaultdict(list)

for f in sys.argv[1:]:
    for test, time in re.findall('([A-Za-z]*\.\w+) \((\d+) ms\)', open(f).read()):
        # print test, time
        stats[test].append(int(time))

for test in sorted(stats.keys()):
    results = sorted(stats[test])
    n = len(results)
    print "%-40s [ms] : %3d min %3d max %3d terc. |%d|" % (
        test, results[0], results[-1], results[n/3], n
    )
