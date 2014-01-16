#!/usr/bin/env python

import os
import re
import sys

# arguments: path to search, substring to find in changes

target, query = sys.argv[1:]

rev = re.compile('^r(\d+)', re.MULTILINE)

log = os.popen('svn log -q %s' % target).read()

revisions = rev.findall(log)

print 'Searching through %d revisions...' % len(revisions)


for r in revisions:
    print "Revision %s:" % r,
    # -x -U4 --diff-cmd=diff
    cmd = 'svn diff -c %s %s' % (r, target)
    print cmd
    diff = os.popen(cmd).read()
    # print '\n', diff
    if diff.find(query) == -1:
        print 'not found.'
        continue
    print os.popen('svn log -r %s %s' % (r, target)).read()
    print diff
    print '-' * 60
    sys.stdout.flush()

