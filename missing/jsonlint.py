#!/usr/bin/env python

from __future__ import print_function

import argparse
import glob
import itertools
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="*", help="files or glob expressions to process")
parser.add_argument(
    "--write-back",
    "--inplace",
    "-w",
    "-i",
    action="store_true",
    help="overwrite existing files",
)
args = parser.parse_args()


def rglob(expr):
    if "**" in expr:
        return glob.glob(expr, recursive=True)
    return glob.glob(expr)


files = list(itertools.chain.from_iterable(map(rglob, args.files)))

if len(files) >= 1:
    for filename in args.files:
        with open(filename) as f:
            json_object = json.load(f)
        if args.write_back:
            with open(filename, "w") as f:
                json.dump(json_object, f, indent=2, sort_keys=True)
        else:
            if len(files) > 1:
                print(filename)
            print(json.dumps(json_object, indent=2, sort_keys=True))
else:
    input_json = sys.stdin.read()
    print(json.dumps(json.loads(input_json), indent=2, sort_keys=True))
