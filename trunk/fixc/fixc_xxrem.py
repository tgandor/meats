#!/usr/bin/env python

import sys
import re

# determine the input
try:
    source = open(sys.argv[1])
except:
    source = sys.stdin

# catch lines with trailing //-comments
line = re.compile("([\t ]*)([^ \t].*)(// ?)(.*)([\r\n]*)")

# move to preceding line
for l in source.readlines():
    m = line.match(l)
    if m:
        sys.stdout.write(
            "%s// %s%s%s%s%s" % tuple(m.group(g) for g in (1,4,5,1,2,5)))
    else:
        sys.stdout.write(l)

