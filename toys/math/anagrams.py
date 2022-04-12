#!/usr/bin/env python

"""Anagram finder."""

import argparse
import re
import sys
from itertools import groupby


parser = argparse.ArgumentParser()
parser.add_argument("-N", type=int, default=10)
parser.add_argument("input", default="-", nargs="?")
args = parser.parse_args()

badchars = re.compile(r"[-,\.]")


def normalize(s):
    s = badchars.sub("", s)
    return "".join(sorted(s.lower()))


source = open(args.input) if args.input != "-" else sys.stdin
lines = sorted(map(str.strip, source.readlines()), key=normalize)
groups = []

for key, group in groupby(lines, key=normalize):
    words = list(group)
    groups.append((len(words), words))

groups.sort(reverse=True)

for i, (n, group) in zip(range(args.N), groups):
    print(f"{i+1} ({n}):\n  {group}")
