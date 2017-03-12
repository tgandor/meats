#!/usr/bin/env python

from __future__ import print_function

import os
import sys
# TODO: import argparse

length = int(sys.argv[1])

for f in sys.argv[2:]:
    prefix = f[:length]
    if not os.path.isdir(prefix):
        os.mkdir(prefix)
    os.rename(f, os.path.join(prefix, f))
    print(f, '->', os.path.join(prefix, f))

