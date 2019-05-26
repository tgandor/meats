#!/usr/bin/env python

from __future__ import division

"""
Show a progress bar of seconds.

Say you're downloading 2.4 GB as 2 MB/s:

    python progress.py 2400 2

- it's roughly 20 mins.
"""

import argparse
import time
import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('n', help='Number of items to process')
parser.add_argument('n_per_second', nargs='?', default='1', help='Speed per second')
args = parser.parse_args()

# TODO: human notation parsing?
n = int(args.n)
n_per_second = int(args.n_per_second)

t = tqdm.tqdm(total=n)
for _ in range(n // n_per_second + 1):
    time.sleep(1)
    t.update(n_per_second)
