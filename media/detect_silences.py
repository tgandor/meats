#!/usr/bin/env python

import argparse
import itertools as it
from os import system
from os.path import splitext, exists

import numpy as np
from scipy.io import wavfile

# this code might have some pcm_s16le (stereo?) assumptions built in...

parser = argparse.ArgumentParser()
parser.add_argument("--min-silence", "-m", type=float, default=0.2)
parser.add_argument("--min-amp", type=int, default=1000)
parser.add_argument("file")
args = parser.parse_args()

if not args.file.lower().endswith('.wav'):
    wave_file = splitext(args.file)[0] + '.wav'
    if not exists(wave_file):
        print(f"Warning: {wave_file} does not exist, creating...")
        system(f'ffmpeg -i "{args.file}" "{wave_file}"')
else:
    wave_file = args.file

rate, data = wavfile.read(wave_file)
low = np.abs(data[:, 0]) // args.min_amp
limit = args.min_silence * rate

L = pos = 0

for k, v in it.groupby(low):
    pos += L
    L = len(list(v))
    if L < limit:
        continue
    print(f"{pos}:{pos+L}: [{k}] * {L} (at {pos/rate:.2f}, {L/rate:.2f}s)")
