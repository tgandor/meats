#!/usr/bin/env python

import sys
import re

# determine the input
try:
    source = open(sys.argv[1])
except:
    source = sys.stdin

# catch lines with trailing //-comments
op = re.compile("([^ ])(<<|>>)([^ ])")

# move to preceding line
sys.stdout.write(
    op.sub(lambda m: "%s %s %s" % m.groups(), source.read())
)
