#!/usr/bin/env python

import argparse
import time
import tqdm


def count(n):
    """Generates a range(n), but not a list or range object."""
    for i in range(n):
        yield i
    

parser = argparse.ArgumentParser()
parser.add_argument('--count', '-n', default=60)
parser.add_argument('--interactive', '-i', action='store_true')
args  = parser.parse_args()

for i in tqdm.tqdm(count(args.count) if args.interactive else range(args.count)):
    time.sleep(1)

