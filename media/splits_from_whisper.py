#!/usr/bin/env python

import argparse
import json
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("json_file")
parser.add_argument("split_keyword")
parser.add_argument("--exclude", "-x")
parser.add_argument("--process", "-p", help="file_to_process using ~/split_video.py")
parser.add_argument("--ci", "-i", action="store_true")
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()

key = args.split_keyword.lower() if args.ci else args.split_keyword

with open(args.json_file) as jsf:
    data = json.load(jsf)

splits = []

for segment in data["segments"]:
    text = segment["text"].lower() if args.ci else segment["text"]
    if args.exclude and args.exclude in text:
        continue
    if key in text:
        splits.append(segment["start"])
        if args.verbose:
            print(segment)

print(" ".join(str(s) for s in splits))

if args.process:
    # Is this really how code re-use should work?
    splitter = os.path.join(os.path.dirname(__file__), "split_video.py")
    os.system(
        " ".join([sys.executable, splitter, args.process] + [str(s) for s in splits])
    )
