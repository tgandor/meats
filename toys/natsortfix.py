#!/usr/bin/env python

import sys
import os
import re

files = sys.argv[1:]

with_num = sorted([ (int(re.search('\d+', f).group()), f) for f in files])

maxnum = with_num[-1][0]
format_chars = len(str(maxnum))
fmt = "%0"+str(format_chars)+"d"

for n, f in with_num:
    newf = re.sub('\d+', fmt%n, f, 1)
    if newf != f:
        if os.path.exists(newf):
            print "Error: %s - file already exists!" % newf
            continue
        print f, '->', newf
        os.rename(f, newf)
