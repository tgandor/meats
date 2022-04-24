#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file1")
parser.add_argument("file2")
parser.add_argument(
    "--common", "-c", action="store_true", help="set intersection (default: difference)"
)
parser.add_argument("--reverse", "-r", action="store_true")
args = parser.parse_args()

words1 = set(open(args.file1).read().split())
words2 = set(open(args.file2).read().split())

if args.reverse:
    words1, words2 = words2, words1

if args.common:
    result = sorted(words1 & words2)
    print("Common words ({}):".format(len(result)))
else:
    result = sorted(words1 - words2)
    print(
        "Words only in {} ({}):".format(
            args.file2 if args.reverse else args.file1, len(result)
        )
    )

for word in result:
    print(word)
