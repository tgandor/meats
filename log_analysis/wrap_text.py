#!/usr/bin/env python

"""
I think this should be the default behavior when running the `textwrap` module.
Instead, this is what happens:
$ python -m textwrap
Hello there.
  This is indented.
"""

import argparse
import sys
import textwrap as tw

parser = argparse.ArgumentParser()
parser.add_argument("--width", "-w", type=int, default=100)
args = parser.parse_args()

while line := sys.stdin.readline():
    print("\n".join(tw.wrap(line.strip(), width=args.width)))
