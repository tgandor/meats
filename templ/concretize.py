#!/usr/bin/env python

import sys
import os

replacement = next((arg for arg in sys.argv if not os.path.exists(arg)), None)

if not replacement:
    print("Usage: {0} REPLACEMENT FILE...".format(sys.argv[0]))
    exit()

for target in filter(os.path.exists, sys.argv[1:]):
    destination = os.path.basename(target).replace('Empty', replacement)
    if os.path.exists(destination):
        print("File '{0}' exists. Not generating.".format(destination))
        continue
    contents = open(target).read().replace('Empty', replacement)
    print("Generating '{0}'...".format(destination))
    open(destination, 'w').write(contents)
