#!/usr/bin/env python

import sys
import os
import re

try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--property", type=str, help="SVN property name (default: svn:mergeinfo)", default='svn:mergeinfo')
    parser.add_argument('--minrev', type=int, default=0) 
    parser.add_argument('--maxrev', type=int, default=0) 
    parser.add_argument('--short', action='store_true')
    args = parser.parse_args()
    prop = args.property
    minrev = args.minrev
    maxrev = args.maxrev
    short = args.short
except ImportError:
    prop = sys.argv[1]
    minrev = 0
    maxrev = 0
    short = False

run = lambda cmd: os.popen(cmd).read()
val = lambda rev: run('svn pg %s -r %d' % (prop, rev))

if not maxrev:
    maxrev = int(re.search('r(\d+)', run('svn log -r HEAD:1 -l 1')).group(1))
if not minrev:
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

def diff(newval, oldval):
    nlines = newval.strip().split('\n')
    olines = oldval.strip().split('\n')
    ins = set(nlines) - set(olines)
    out = set(olines) - set(nlines)
    return '\n'.join(
        [ '-%s' % line for line in olines if line in out ] +
        [ ('+%s' if line in ins else ' %s') % line 
            for line in (ins if short else nlines) 
        ]
    )

history = [(0, 0, '')]
left = minrev
while True:
    right = find_end(left)
    value = val(left)
    print "%d-%d" % (left, right)
    print diff(value, history[-1][2])
    print '-'*40
    history.append((left, right, value))
    if right == maxrev:
        break
    left = right + 1
