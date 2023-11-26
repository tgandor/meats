#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("video_file")
parser.add_argument("splits", nargs="+")
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
args = parser.parse_args()

basename, ext = os.path.splitext(args.video_file)

startpos = "0"
chunk = 1


def _gen_splits(splits):
    for split in splits:
        if os.path.exists(split):
            for line in open(split):
                yield line.split()[0]
            continue
        yield split


splits = list(_gen_splits(args.splits))

if args.fps:
    splits = [int(split) / args.fps for split in splits]

codec = "" if args.reencode else "-c copy"

for split in splits:
    if args.floats:
        command = 'ffmpeg -hide_banner -ss {} -i "{}" {} -map_metadata 0 -to {} "{}_{}{}"'.format(
            startpos,
            args.video_file,
            codec,
            float(split) - float(startpos),
            basename,
            chunk,
            ext,
        )
    else:
        command = 'ffmpeg -hide_banner -ss {} -to {} -i "{}" {} -map_metadata 0 "{}_{}{}"'.format(
            startpos,
            split,
            args.video_file,
            codec,
            basename,
            chunk,
            ext,
        )

    print(command)
    os.system(command)
    startpos = split
    chunk += 1
    print(("=" * 60 + "\n") * 3)

# final chunk, without `-to`, works for both ffmpeg 'versions'`
command = 'ffmpeg -hide_banner -ss {} -i "{}" -c copy -map_metadata 0 "{}_{}{}"'.format(
    startpos, args.video_file, basename, chunk, ext
)
print(command)
os.system(command)
