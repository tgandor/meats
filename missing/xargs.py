#!/usr/bin/env python

import os
import sys

# take all, arguments[:None] == arguments[:]
batch_size = None

if len(sys.argv) < 2:
    print('Usage: xargs.py <command_prefix>')
    exit()

argv = sys.argv[1:]

if argv[0] == '-n' and len(argv) > 1:
    batch_size = int(argv[1])
    argv = argv[2:]

prefix = ' '.join(argv) + ' '

arguments = [argument.strip() for argument in sys.stdin.readlines()]

while arguments:
    batch = arguments[:batch_size]
    command = prefix + ' '.join(batch)
    print(command)
    os.system(command)
    arguments = arguments[len(batch):]
