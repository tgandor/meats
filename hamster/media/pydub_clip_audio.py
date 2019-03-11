#!/usr/bin/env python3

from __future__ import print_function

"""
Script to cut of all mp3 files in a directory by a specified amount of seconds.
"""

import argparse
import glob
import os

import pydub
import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--leading', '-ss', default=0, help='Leading seconds to cut off', type=float)
parser.add_argument('--trailing', '-tt', default=0, help='Trailing seconds to cut off', type=float)
args = parser.parse_args()


def strip_song(song, before_s=0, after_s=0):
    if not (before_s or after_s):
        return song
    end = -int(after_s * 1000) if after_s else None
    stripped = song[int(before_s*1000):end]
    return stripped


os.makedirs('output', exist_ok=True)

files = sorted(glob.glob('*.mp3'))

for name in tqdm.tqdm(files):
    song = pydub.AudioSegment.from_file(name)
    cut = strip_song(song, args.leading, args.trailing)
    cut.export(os.path.join('output', name))
    tqdm.tqdm.write(f'{name}: file cropped from {len(song)//1000} to {len(cut)//1000}')
