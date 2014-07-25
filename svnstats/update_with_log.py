#!/usr/bin/env python

import os
import re

revision = re.compile('Revision: (\d+)')
last_change_rev = re.compile('Rev: (\d+)')

info_before = os.popen('LANG=C svn info').read()
result = os.system('svn up')
info_after = os.popen('LANG=C svn info').read()

revision_before = revision.search(info_before).group(1)
revision_after = revision.search(info_after).group(1)

if revision_after == revision_before:
    print 'No changes, still at revision %s.' % revision_after
    exit(1)

revision_last = last_change_rev.search(info_after).group(1)

if int(revision_last) <= int(revision_before):
    print 'Updated from %s to %s, but last change here was in %s' % (
        revision_before, revision_after, revision_last)
    exit(1)

print 'Updated from %s to %s.' % (revision_before, revision_after),
if int(revision_last) < int(revision_after):
    print '(last change: %s)' % revision_last
else:
    print '(most current)'

print 'Log of updates:'

os.system('svn log -r %d:%s -v' % (int(revision_before)+1, revision_last))
