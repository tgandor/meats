#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('video_file')
parser.add_argument('--pos', type=float, default=3.5, help='time offset of frame')
args = parser.parse_args()

output = os.path.splitext(args.video_file)[0] + '.jpg'
os.system(
    f'ffmpeg -hide_banner -ss {args.pos} -i "{args.video_file}" '
    f'-vframes 1 -f image2 "{output}"'
)
