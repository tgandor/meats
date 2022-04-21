#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file1")
parser.add_argument("file2")
parser.add_argument("--common", "-c", action="store_true", help="set intersection (default: difference)")
args = parser.parse_args()

words1 = set(open(args.file1).read().split())
words2 = set(open(args.file2).read().split())

if args.common:
    print("Common words:")
    for word in sorted(words1 & words2):
        print(word)
else:
    print("Words only in {}:".format(args.file1))
    for word in sorted(words1 - words2):
        print(word)
