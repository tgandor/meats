#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('video_file')
parser.add_argument('splits', nargs='+')
args = parser.parse_args()

basename, ext = os.path.splitext(args.video_file)

startpos = '0'
chunk = 1

for split in args.splits:
    command = 'ffmpeg -hide_banner -ss {} -to {} -i "{}" -c copy -map_metadata 0 "{}_{}{}"'.format(
        startpos, split, args.video_file, basename, chunk, ext
    )
    print(command)
    os.system(command)
    startpos = split
    chunk += 1
    print(('='*60 + '\n') * 3)

# final chunk
command = 'ffmpeg -hide_banner -ss {} -i "{}" -c copy -map_metadata 0 "{}_{}{}"'.format(
    startpos, args.video_file, basename, chunk, ext
)
print(command)
os.system(command)
