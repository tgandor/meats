#!/usr/bin/env python

import argparse

import numpy as np
from scipy.io import wavfile


parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+")
parser.add_argument("--sort", "-s", action="store_true")
args = parser.parse_args()

results = []
for path in args.files:
    rate, data = wavfile.read(path)
    rmse = np.mean(data.astype(np.float32) ** 2) ** 0.5
    results.append((rmse, path))

if args.sort:
    results.sort()

for rmse, path in results:
    print(f"{path}: {rmse:8.2f}")
