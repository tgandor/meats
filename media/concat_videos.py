#!/usr/bin/env python

# Credits: https://www.markheath.net/post/cut-and-concatenate-with-ffmpeg

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("chunk_files", nargs="+")
parser.add_argument("--output", "-o", default="joined.mp4")
args = parser.parse_args()

with open('inputs.txt', 'w') as f:
    for fn in args.chunk_files:
        f.write(f"file '{fn}'\n")

cmd = f"ffmpeg -f concat -i inputs.txt -c copy {args.output}"
print(cmd)
os.system(cmd)
