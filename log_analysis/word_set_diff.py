#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file1")
parser.add_argument("file2")
parser.add_argument(
    "--common", "-c", action="store_true", help="set intersection (default: difference)"
)
args = parser.parse_args()

words1 = set(open(args.file1).read().split())
words2 = set(open(args.file2).read().split())

if args.common:
    result = sorted(words1 & words2)
    print("Common words ({}):".format(len(result)))
else:
    result = sorted(words1 - words2)
    print("Words only in {} ({}):".format(args.file1, len(result)))

for word in result:
    print(word)
