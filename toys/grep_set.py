#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('search_letters', type=str)
parser.add_argument('--count', '-c', action='store_true', help='Print match numbers')
args = parser.parse_args()

template = set(args.search_letters.lower())

count = 0
for line in sys.stdin:
    for word in map(str.strip, line.split(',')):
        if word.startswith('kasa'):
            print('Comparing', set(word.lower()), template)
        if set(word.lower()) <= template:  # set(word.lower()).issubset(template) - better?
            count += 1
            if count: 
                print(count, word)
            else:
                print(word)
