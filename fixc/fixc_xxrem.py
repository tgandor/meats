#!/usr/bin/env python

import sys
import re

# catch lines with trailing //-comments
line = re.compile("^([\t ]*)([^ \t].*)(// ?)([^\r\n]*)(\r?\n?)", re.M)

def process_line_comments(bulk):
    # move to preceding line
    return line.sub(lambda m: "%s// %s%s%s%s%s" % tuple(m.group(g) for g in (1,4,5,1,2,5)), bulk)

# determine the input

if len(sys.argv) < 2:
    sys.stdout.write(process_line_comments(sys.stdin.read()))
else:
    for f in sys.argv[1:]:
        data = open(f).read()
        changed = process_line_comments(data)
        if data <> changed:
            open(f+"~", "w").write(data)
            open(f, "w").write(changed)

        

