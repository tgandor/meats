#!/usr/bin/env python

from __future__ import print_function

import argparse
import itertools
import sys

parser = argparse.ArgumentParser()
parser.add_argument('search_letters', type=str)
parser.add_argument('files', type=str, nargs='*')
parser.add_argument('--count', '-c', action='store_true', help='Print match numbers')
args = parser.parse_args()

template = set(args.search_letters.lower())

def get_input(files):
    if not files:
        return sys.stdin
    return itertools.chain.from_iterable(map(open, files))


count = 0
for line in get_input(args.files):
    for word in map(str.strip, line.split(',')):
        if set(word.lower()) <= template:  # set(word.lower()).issubset(template) - better?
            count += 1
            if count: 
                print(count, word)
            else:
                print(word)
