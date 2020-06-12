#!/usr/bin/env python

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('expression', help='The expression to evaluate on the JSON object, e.g. x["name"]')
parser.add_argument('files', nargs='+')
parser.add_argument('--name', '-n', action='store_true', help='print filename before value')
parser.add_argument('--skip-none', '-q', action='store_true', help='print only when result != None')
args = parser.parse_args()

for f in args.files:
    with open(f) as stream:
        x = json.load(stream)

    result = eval(args.expression)

    if args.skip_none and result is None:
        continue

    if args.name:
        print(f, result)
    else:
        print(result)

