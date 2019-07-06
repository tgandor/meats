#!/usr/bin/env python

import os
import datetime

from mutagen.mp3 import MP3

mp3s = []

for directory, _, files in os.walk('.'):
    for basename in files:
        filename = os.path.join(directory, basename)
        if basename.lower().endswith('.mp3'):
            audio = MP3(filename)
            # print(basename, audio.info.length)
            mp3s.append((datetime.timedelta(seconds=int(audio.info.length)), filename))

mp3s.sort()
total = datetime.timedelta()

for i, (duration, filename) in enumerate(mp3s):
    print(i+1, duration, filename)
    total += duration

print('Total:', total)
