#!/usr/bin/env python

import argparse
import json
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("split_keyword")
parser.add_argument("json_files", nargs="+")
parser.add_argument("--exclude", "-x", help="negative keyword to ignore when ")
parser.add_argument(
    "--process", "-p", help="file extension to replace .json and run ./split_video.py"
)
parser.add_argument("--case-sensitive", "-c", action="store_true")
parser.add_argument("--verbose", "-v", action="store_true")
parser.add_argument(
    "--text", "-t", action="store_true", help="print matching segment texts"
)
args = parser.parse_args()
ci = not args.case_sensitive
key = args.split_keyword.lower() if ci else args.split_keyword

for json_file in args.json_files:
    if args.text:
        print(json_file)
    with open(json_file) as jsf:
        data = json.load(jsf)

    splits = []

    for segment in data["segments"]:
        text = segment["text"].lower() if ci else segment["text"]
        if args.exclude and args.exclude in text:
            continue
        if key in text:
            splits.append(segment["start"])
            if args.verbose:
                print(segment)
            if args.text:
                print(segment["text"])

    print(" ".join(str(s) for s in splits))

    if args.process:
        # Is this really how code re-use should work?
        splitter = os.path.join(os.path.dirname(__file__), "split_video.py")
        target = json_file.replace("json", args.process)
        if not os.path.exists(target):
            raise ValueError(f"Target file {target} not found!")

        os.system(
            " ".join([sys.executable, splitter, target] + [str(s) for s in splits])
        )
