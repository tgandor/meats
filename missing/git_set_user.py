#!/usr/bin/env python

import os
import sys

if len(sys.argv) > 1:
    source_dir = sys.argv[1]
    target_dir = os.getcwd()
else:
    source_dir = target_dir = os.getcwd()

os.chdir(source_dir)
last_commit = os.popen("git log -1").readlines()
author = last_commit[1].split()

os.chdir(target_dir)
cmd = 'git config user.name "{}"'.format(' '.join(author[1:-1]))
print(cmd)
os.system(cmd)
cmd = 'git config user.email "{}"'.format(author[-1][1:-1])
print(cmd)
os.system(cmd)
