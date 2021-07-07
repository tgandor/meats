#!/usr/bin/env python

import argparse
import gzip
import pickle
import pprint

parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("--force", "-f", action="store_true")
args = parser.parse_args()

if not args.force:
    print("WARNING: can you trust this pickle? If so, specify: --force")
    exit()

opener = gzip.open if args.filename.endswith("gz") else open

with opener(args.filename, "rb") as pkl:
    value = pickle.load(pkl)
    pprint.pprint(value)
