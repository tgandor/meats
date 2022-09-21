#!/usr/bin/env python

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("n", type=int, nargs="?", default=170)
parser.add_argument("--show", "-v", action="store_true")
args = parser.parse_args()

for line in sys.stdin:
    if len(line) > args.n:
        if args.show:
            sys.stdout.write(line[:args.n-3] + "...\n")
        continue
    sys.stdout.write(line)
