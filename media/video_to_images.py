#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("video")
parser.add_argument("--dedup", "-d", action="store_true", help="drop duplicate frames")
parser.add_argument("--nvdec", "-nv", action="store_true")
parser.add_argument("--output", "-o", help="output directory for images")
parser.add_argument("--frames", "-n", type=int, help="limit frames number")
parser.add_argument("--start", "-ss")
parser.add_argument(
    "--quality", "-q", type=int, help="quality (JPG) 1(best) - 31(worst)"
)
parser.add_argument("--format", "-f", default="png")
args = parser.parse_args()

out_dir = args.output if args.output else os.path.splitext(args.video)[0]
os.makedirs(out_dir, exist_ok=True)

command = "ffmpeg -hide_banner"

if args.nvdec:
    command += " -hwaccel nvdec"

if args.start:
    command += f" -ss {args.start}"

command += f' -i "{args.video}"'

if args.dedup:
    command += " -vf mpdecimate"

if args.frames:
    command += f" -vframes {args.frames}"

if args.quality:
    if not (1 <= args.quality <= 31):
        print(f"Warning, quality {args.quality} ignored. Required range 1--31")
    else:
        if args.quality == 1:
            # https://stackoverflow.com/questions/10225403/how-can-i-extract-a-good-quality-jpeg-image-from-a-video-file-with-ffmpeg
            command += " -qmin 1"
        command += f" -q:v {args.quality}"

command += f' "{out_dir}/%06d.{args.format}"'

print(command)
os.system(command)
