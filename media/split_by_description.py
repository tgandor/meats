#!/usr/bin/env python

import argparse
import os
from dataclasses import dataclass

parser = argparse.ArgumentParser()
parser.add_argument("video_file")
parser.add_argument("splitfile")
parser.add_argument(
    "--fps", "-f", type=float, help="treat splits as frame numbers, compute times"
)
parser.add_argument(
    "--floats",
    action="store_true",
    help="all splits are floats in seconds. For legacy ffmpeg (OK with --fps/-f).",
)
parser.add_argument(
    "--reencode",
    "-r",
    action="store_true",
    help="don't use -c copy (may be more exact)",
)
parser.add_argument("--dry-run", "-n", action="store_true")
args = parser.parse_args()


@dataclass
class Split:
    start: str
    end: str
    description: str


def parse_splits(path):
    data = open(path).read().strip().split("\n")
    result = []
    for l1, l2 in zip(data, data[1:]):
        words = l1.split()
        if len(words) > 1 and words[1] == "--":
            continue
        end = l2.split()[0]
        result.append(Split(f"-ss {words[0]}", f"-to {end}", "_".join(words[1:])))
    words = data[-1].split()
    if len(words) == 1 or words[1] != "--":
        result.append(Split(f"-ss {words[0]}", "", "_".join(words[1:])))
    return result


def main():
    _, ext = os.path.splitext(args.video_file)
    splits = parse_splits(args.splitfile)
    width = len(str(len(splits)))
    codec = "" if args.reencode else "-c copy"

    for chunk, split in enumerate(splits, 1):
        command = (
            f'ffmpeg -hide_banner {split.start} {split.end} -i "{args.video_file}"'
            + f' {codec} -map_metadata 0 "{chunk:0{width}d}_{split.description}{ext}"'
        )
        print(command)
        if not args.dry_run:
            os.system(command)
        print(("=" * 60 + "\n") * 2)


if __name__ == "__main__":
    main()
