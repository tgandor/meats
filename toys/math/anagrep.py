#!/usr/bin/env python

"""Anagram grep."""

import sys


def normalize(s):
    return ''.join(sorted(s.lower()))

pattern = normalize(sys.argv[1])

while True:
    line = sys.stdin.readline().strip()
    if not line:
        break
    if normalize(line) == pattern:
        print(line)
