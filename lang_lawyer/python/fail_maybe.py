#!/usr/bin/env python

import argparse
import random
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--max-status", "-n", type=int, default=3)
parser.add_argument("--verbose", "-v", action="store_true")
parser.epilog = "Try: while ! ~/meats/lang_lawyer/python/fail_maybe.py -v ; do : ; done"
args = parser.parse_args()

status = random.randint(0, args.max_status)
if args.verbose:
    print("Returning:", status)
sys.exit(status)
