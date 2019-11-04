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
parser.add_argument('--format', default='{:02d}', help='subfolder name format')
args = parser.parse_args()


def show_preview(filename):
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    cv2.imshow('image', image)
    ret = cv2.waitKey(0) & 0xff
    if ret in [ord('n'), 32, ord('j')]:
        return 1

    if ret in [ord('p'), 8, ord('k')]:
        return -1

    if ret in [ord('q'), 27]:
        cv2.destroyAllWindows()
        sys.exit()

    return 0


def get_next_folder(prev_folder, format):
    while True:
        prev_folder += 1
        if not os.path.exists(format.format(prev_folder)):
            return prev_folder


files = sorted(itertools.chain.from_iterable(map(glob.glob, args.files)))
next_folder = get_next_folder(0, args.format)

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

    folder = args.format.format(next_folder)
    if not os.path.exists(folder):
        os.makedirs(folder)

    for filename in files[:idx+1]:
        print(filename, '->', folder)
        os.rename(filename, os.path.join(folder, filename))

    files = files[idx+1:]
    next_folder = get_next_folder(next_folder, args.format)
