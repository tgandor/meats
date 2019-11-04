#!/usr/bin/env python

import argparse
import glob
import itertools
import os
import re
import sys

import cv2


parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
args = parser.parse_args()

# TODO: quitting, restarting, scale? (or window mode)


def show_preview(filename):
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    cv2.imshow('image', image)
    ret = cv2.waitKey(0) & 0xff
    if ret in [ord('n'), 32, ord('j')]:
        return 1

    if ret in [ord('p'), 8, ord('k')]:
        return -1

    return 0

files = sorted(itertools.chain.from_iterable(map(glob.glob, args.files)))
next_folder = 1

while files:
    idx = 0

    while True:
        di = show_preview(files[idx])
        if di == 0:
            break

        idx += di

        if idx < 0:
            idx = 0
        elif idx >= len(files):
            idx = len(files)
            break

    folder = '{:02d}'.format(next_folder)
    if not os.path.exists(folder):
        os.makedirs(folder)
    for filename in files[:idx+1]:
        print(filename, '->', folder)
        # os.rename(filename, os.path.join(folder, filename))

    files = files[idx+1:]
