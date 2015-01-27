#!/usr/bin/env python

import os
import sys


def usage():
    print 'choose_files from_directory <number_file|number...>'
    exit()

if len(sys.argv) < 3:
    usage()

from_dir = sys.argv[1]
from_files = sorted(next(os.walk(from_dir))[2])

if os.path.isfile(sys.argv[2]):
    file_indexes = open(sys.argv[2]).read().split()
else:
    file_indexes = sys.argv[2:]

for idx in map(int, file_indexes):
    print '{0}: {1}'.format(idx, from_files[idx])

