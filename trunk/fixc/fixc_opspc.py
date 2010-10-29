#!/usr/bin/env python

import sys
import re

# catch lines with trailing //-comments
op = re.compile("([^ ])(<<|>>)([^ ])")

# move to preceding line
process_ops = lambda data: op.sub(
    lambda m: "%s %s %s" % m.groups(), data)


# determine the input

if len(sys.argv) < 2:
    sys.stdout.write(process_ops(sys.stdin.read()))
else:
    for f in sys.argv[1:]:
        data = open(f).read()
        changed = process_ops(data)
        if data <> changed:
            open(f+"~", "w").write(data)
            open(f, "w").write(changed)

