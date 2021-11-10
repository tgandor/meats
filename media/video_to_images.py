#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("video")
parser.add_argument("--dedup", "-d", action="store_true", help="drop duplicate frames")
parser.add_argument("--output", "-o", help="output directory for images")
parser.add_argument("--frames", "-n", type=int, help="limit frames number")
parser.add_argument("--format", "-f", default="png")
args = parser.parse_args()

out_dir = args.output if args.output else os.path.splitext(args.video)[0]
os.makedirs(out_dir, exist_ok=True)

command = f'ffmpeg -hide_banner -i "{args.video}"'

if args.dedup:
    command += " -vf mpdecimate"

if args.frames:
    command += f" -vframes {args.frames}"

command += f' "{out_dir}/%06d.{args.format}"'

print(command)
os.system(command)
