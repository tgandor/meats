#!/usr/bin/env python

import glob
import os
import sys


def usage():
    print 'chosen_files from_directory chosen_directory'
    exit()

if len(sys.argv) != 3:
    usage()

from_dir, choice_dir = sys.argv[1:]

from_files = sorted(next(os.walk(from_dir))[2])
choice_files = sorted(next(os.walk(choice_dir))[2])

file_indexes = dict(zip(from_files, range(1, len(from_files)+1)))

for f in choice_files:
    print '{0}: {1}'.format(file_indexes[f], f)

