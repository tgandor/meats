#!/usr/bin/env python

import os
import re

diff_header = re.compile(r'diff --git a/(.+) b/\1')
old_mode = re.compile(r'old mode 100(\d{3})')
new_mode = re.compile(r'new mode 100(\d{3})')

path = None
old = None

for line in os.popen('git diff').readlines():
    m = diff_header.match(line)
    if m:
        path = m.group(1)
        old = None
        continue

    m = old_mode.match(line)
    if m:
        old = m.group(1)
        continue

    m = new_mode.match(line)
    if m and path and old:
        command = 'chmod {} {}'.format(old, path)
        print(command)
        os.system(command)
        path = old = None
