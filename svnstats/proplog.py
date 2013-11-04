#!/usr/bin/env python

import sys
import os
import re

prop = sys.argv[1]

run = lambda cmd: os.popen(cmd).read()
val = lambda rev: run('svn pg %s -r %d' % (prop, rev))

maxrev = int(re.search('r(\d+)', run('svn log -r HEAD:1 -l 1')).group(1))
minrev = int(re.search('r(\d+)', run('svn log -r 1:HEAD -l 1')).group(1))
maxval = val(maxrev)

def find_end(startrev):
    curr = val(startrev)
    if curr == maxval:
        return maxrev
    endrev = maxrev
    while True:
        currev = (startrev + endrev) / 2
        # print >>sys.stderr, "Checking %d" % currev
        if val(currev) != curr:
            endrev = currev
        else:
            if val(currev+1) != curr:
                return currev
            startrev = currev

left = minrev
while True:
    right = find_end(left)
    print "%d-%d" % (left, right)
    print val(left)
    if right == maxrev:
        break
    left = right + 1

