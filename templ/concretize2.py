#!/usr/bin/env python

import sys
import os

non_file_args = (arg for arg in sys.argv if not os.path.exists(arg))
pattern = next(non_file_args, None)
replacement = next(non_file_args, None)

if not pattern or not replacement:
    print("Usage: {0} PATTERN REPLACEMENT FILE...".format(sys.argv[0]))
    exit()

for target in filter(os.path.exists, sys.argv[1:]):
    destination = os.path.basename(target).replace(pattern, replacement)
    if os.path.exists(destination):
        print("File '{0}' exists. Not generating.".format(destination))
        continue
    contents = open(target).read().replace(pattern, replacement)
    print("Generating '{0}'...".format(destination))
    open(destination, 'w').write(contents)
