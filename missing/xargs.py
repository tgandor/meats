#!/usr/bin/env python

import os
import sys

if len(sys.argv) < 2:
    print('Usage: xargs.py <command_prefix>')
    exit()

prefix = ' '.join(sys.argv[1:]) + ' '
for argument in sys.stdin.readlines():
    command = prefix + argument.strip()
    print(command)
    os.system(command)
