#!/usr/bin/env python

from __future__ import print_function

import os
import sys
from itertools import islice

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
print(prefix, '...')

arguments = (argument.strip() for argument in sys.stdin)

while True:
    batch = islice(arguments, None, batch_size) # arguments[:batch_size]
    batch_args = ' '.join(batch)
    if not batch_args:
        break
    command = prefix + batch_args
    print(command)
    os.system(command)
    # arguments = arguments[len(batch):]
