#!/usr/bin/env python

from __future__ import print_function

import argparse
import itertools
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--count', '-c', action='store_true', help='Print match numbers')
parser.add_argument('--no-acronyms', action='store_true', help='Exclude words in ALLCAPS')
parser.add_argument('--unique', '-u', action='store_true', help='Ensure unique words')
parser.add_argument('--min-length', type=int, help='Only print words at least that long', default=3)
parser.add_argument('search_letters', type=str)
parser.add_argument('files', type=str, nargs='*')
args = parser.parse_args()

template = set(args.search_letters.lower())

def get_input(files):
    if not files:
        return sys.stdin
    return itertools.chain.from_iterable(map(open, files))


count = 0
seen = set()

for line in get_input(args.files):
    for word in map(str.strip, line.split(',')):
        if args.no_acronyms and word.upper() == word:
            continue
        if len(word) < args.min_length:
            continue
        if set(word.lower()) <= template:  # set(word.lower()).issubset(template) - better?
            if args.unique:
                if word.lower() in seen:
                    continue
                seen.add(word.lower())
            count += 1
            if args.count:
                print(count, word)
            else:
                print(word)
