#!/usr/bin/env python

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('expression', help='The expression to evaluate on the JSON object, e.g. x["name"]')
parser.add_argument('files', nargs='+')
parser.add_argument('--name', '-n', action='store_true', help='print filename before value')
args = parser.parse_args()

for f in args.files:
    with open(f) as stream:
        x = json.load(stream)
    if args.name:
        print(f, eval(args.expression))
    else:
        print(eval(args.expression))

