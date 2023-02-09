#!/usr/bin/env python

import argparse
import itertools as it
from datetime import datetime, timedelta
from os import system
from os.path import splitext, exists

import numpy as np
from scipy.io import wavfile

# this code might have some pcm_s16le (stereo?) assumptions built in...

parser = argparse.ArgumentParser()
parser.add_argument("--min-silence", "-m", type=float, default=0.2)
parser.add_argument("--min-amp", "-a", type=int, default=1000)
parser.add_argument("file")
args = parser.parse_args()


def fmt_pos(pos, rate):
    s = pos / rate
    fmt = "%M:%S.%f"
    if s > 3600:
        fmt = "%H:" + fmt
    return (datetime.fromordinal(1) + timedelta(seconds=s)).strftime(fmt)[:-3]


if not args.file.lower().endswith(".wav"):
    wave_file = splitext(args.file)[0] + ".wav"
    if not exists(wave_file):
        print(f"Warning: {wave_file} does not exist, creating...")
        system(f'ffmpeg -i "{args.file}" "{wave_file}"')
else:
    wave_file = args.file

rate, data = wavfile.read(wave_file)
low = np.abs(data[:, 0]) // args.min_amp
limit = args.min_silence * rate

L = pos = 0
num_sil = 0

for k, v in it.groupby(low):
    pos += L
    L = len(list(v))
    if L < limit:
        continue
    num_sil += 1
    print(f"{num_sil:4d} {fmt_pos(pos, rate)} - {fmt_pos(pos + L, rate)}: {L/rate:.3f} s ([{k}] * {L})")
