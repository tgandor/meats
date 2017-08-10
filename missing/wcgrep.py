#!/usr/bin/env python

from __future__ import print_function

# import argparse
import os
import sys

search = sys.argv[1]

for directory, _, files in os.walk("."):
    if directory[2:].startswith('.'):  # skip .\
        continue
    for f in files:
        if f.startswith('.'):
            continue
        full_name = os.path.join(directory, f)
        # print(full_name)
        with open(full_name) as lines:
            nl = 0
            try:
                for line in lines:
                    nl += 1
                    if search in line:
                        print(full_name, ':', nl, ':', line.rstrip())
            except UnicodeDecodeError:
                print('Error decoding:', full_name, file=sys.stderr)
