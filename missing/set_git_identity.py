#!/usr/bin/env python

import os

last_commit = os.popen("git log -1").readlines()
author = last_commit[1].split()

cmd = 'git config user.name "{}"'.format(' '.join(author[1:-1]))
print(cmd)
os.system(cmd)
cmd = 'git config user.email "{}"'.format(author[-1][1:-1])
print(cmd)
os.system(cmd)
