#!/usr/bin/env python

# this file adds includes for C(++) files
# which use functions from various headers
# without including them.

# usage:
# fixc_includes.py [files.cpp to.cpp repair.cpp]

# modifies inplace if arguments present, otherwise
# processes standart input to standard output

import sys
import re

data = [
    ['stdio.h', ['fflush', 'stdin', 'getchar']]
]

def fix_includes(bulk):
    eol = re.search("[\r\n]+", bulk).group()
    for heading, keywords in data:
        if bulk.find(heading) == -1:
            for word in keywords:
                if bulk.find(word) <> -1:
                    bulk = "#include <%s>%s%s" % (heading, eol, bulk)
                    break
    return bulk
                
if len(sys.argv) < 2:
    sys.stdout.write(fix_includes(sys.stdin.read()))
else:
    for f in sys.argv[1:]:
        contents = open(f).read()
        open(f+'~', 'w').write(contents)
        open(f, 'w').write(fix_includes(contents))
