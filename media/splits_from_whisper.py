#!/usr/bin/env python

import argparse
import json
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("split_keyword")
parser.add_argument("json_files", nargs="+")
parser.add_argument(
    "--exclude",
    "-x",
    help="negative [filenames with] substring(s) to ignore",
    nargs="*",
)
parser.add_argument(
    "--process", "-p", help="file extension to replace .json and run ./split_video.py"
)
parser.add_argument(
    "--repair",
    action="store_true",
    help="fix chunks which had -to as ffmpeg output option.",
)
parser.add_argument("--case-sensitive", "-c", action="store_true")
parser.add_argument("--verbose", "-v", action="store_true")
parser.add_argument(
    "--text", "-t", action="store_true", help="print matching segment texts"
)
parser.add_argument(
    "--descriptions",
    "-d",
    action="store_true",
    help="generate .txt files for each split's beginning",
)
args = parser.parse_args()
ci = not args.case_sensitive
key = args.split_keyword.lower() if ci else args.split_keyword


class Excludes:
    def __init__(self, excludes, case_sensitive) -> None:
        self.excludes = []
        if excludes is None:
            return
        for item in excludes:
            if os.path.exists(item):
                self.excludes.extend(line.strip() for line in open(item))
            else:
                self.excludes.append(item)
        if not case_sensitive:
            self.excludes = [item.lower() for item in self.excludes]

    def match(self, candidate):
        return any(item in candidate for item in self.excludes)


excludes = Excludes(args.exclude, args.case_sensitive)


for json_file in args.json_files:
    if args.text:
        print(json_file)
    with open(json_file) as jsf:
        data = json.load(jsf)

    splits = []
    descriptions = [data["segments"][0]["text"]]

    for segment in data["segments"]:
        text = segment["text"].lower() if ci else segment["text"]
        if excludes.match(text):
            if args.verbose:
                print(f"IGNORING: {segment['text']}")
            continue
        if key in text:
            splits.append(segment["start"])
            if args.verbose:
                print(segment)
            if args.text:
                print(segment["text"])
            descriptions.append(segment["text"])

    print(" ".join(str(s) for s in splits))

    if args.descriptions:
        basename, ext = os.path.splitext(json_file)
        assert ext == ".json"
        for chunk, description in enumerate(descriptions, start=1):
            filename = (
                f"{basename}_{chunk}.txt"
                if len(descriptions) > 1
                else f"{basename}.txt"
            )
            print(f"{filename}: {description}")
            with open(filename, "w") as dfile:
                print(description, file=dfile)

    if args.repair:
        assert args.process, "Repair requires and extension to process"
        basename, ext = os.path.splitext(json_file)
        assert ext == ".json"

        if len(splits) < 2:
            print(f"INFO: not enough splits for {json_file}")
            continue

        os.makedirs("bak", exist_ok=True)\

        for chunk, (begin, end) in enumerate(zip(splits, splits[1:]), 2):
            filename = f"{basename}_{chunk}.{args.process}"
            backup = os.path.join("bak", filename)
            os.rename(filename, backup)
            command = f'ffmpeg -hide_banner -i "{backup}" -c copy -to {end-begin} "{filename}"'
            print(command)
            os.system(command)

        continue

    if args.process:
        # Is this really how code re-use should work?
        if not splits:
            print(f"WARNING: no splits for {json_file}")
            continue
        splitter = os.path.join(os.path.dirname(__file__), "split_video.py")
        target = json_file.replace("json", args.process)
        if not os.path.exists(target):
            raise ValueError(f"Target file {target} not found!")

        os.system(
            " ".join(
                [sys.executable, splitter, target, "--floats"]
                + [str(s) for s in splits]
            )
        )
