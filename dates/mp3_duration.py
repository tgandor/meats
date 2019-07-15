#!/usr/bin/env python

import argparse
import os
import datetime

from mutagen.mp3 import MP3

parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default='.')
parser.add_argument('--no-sort', '-n', action='store_true')
args = parser.parse_args()

mp3s = []

for directory, _, files in os.walk(args.path):
    for basename in sorted(files):
        filename = os.path.join(directory, basename)
        if basename.lower().endswith('.mp3'):
            try:
                audio = MP3(filename)
                # print(basename, audio.info.length)
                mp3s.append((datetime.timedelta(seconds=int(audio.info.length)), filename))
            except:
                print('Processing', filename, 'failed!')

if not args.no_sort:
    mp3s.sort()

total = datetime.timedelta()

for i, (duration, filename) in enumerate(mp3s):
    print(i+1, duration, filename)
    total += duration

print('Total:', total)
