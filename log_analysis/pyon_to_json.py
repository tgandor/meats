#!/usr/bin/env python

import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--save", "-w", action="store_true")
args = parser.parse_args()

pyon = open(args.input).read()
data = eval(pyon)

if args.save:
    base, _ = os.path.splitext(args.input)
    with open(base + ".json", "w") as js:
        json.dump(data, js, indent=2)
else:
    print(json.dumps(data, indent=2))
