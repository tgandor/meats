#!/usr/bin/env python

import argparse
import os

import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-v3', action='store_true', help='compare 3-way')
parser.add_argument('--full', action='store_true', help='display full filenames in window title')
parser.add_argument('--delay', type=int, help='wait between frames [ms]. 0 = forever', default=40)
parser.add_argument('--vcrop', '-H', type=int, help='crop frames to H lines of image')
parser.add_argument('--hcrop', '-W', type=int, help='crop frames to W columns of image')
parser.add_argument('files', nargs='*')
args = parser.parse_args()

paths = args.files

if not paths:
    paths = [
        input('Video path {}: '.format(i))
        for i in range(3 if args.v3 else 2)
    ]

readers = [cv2.VideoCapture(path) for path in paths]

names = paths if args.full else map(os.path.basename, paths)
window = ' vs '.join(names)

cv2.namedWindow(window, cv2.WINDOW_NORMAL)
pause = False

while True:
    rets_frames = [cap.read() for cap in readers]

    if not all(ret for ret, _ in rets_frames):
        print('Some streams failed to read next frame.')
        break

    frames = [frame for _, frame in rets_frames]

    if args.hcrop:
        frames = [frame[:, :args.hcrop] for frame in frames]

    if args.vcrop:
        frames = [frame[:args.vcrop] for frame in frames]

    assert len({frame.shape for frame in frames}) == 1, 'Frame shapes must be equal'

    tiles = np.hstack(frames)

    cv2.imshow(window, tiles)

    ret = cv2.waitKey(args.delay)

    if ret & 0xff in (ord('q'), 27):
        break

    elif ret & 0xff == ord(' ') or ret & 0xff == ord('.')  or pause:
        pause = True
        while True:
            ret = cv2.waitKey(1000)
            if ret & 0xff == ord(' '):
                pause = False
                break
            if ret & 0xff == ord('.'):
                break
            if ret & 0xff in (ord('q'), 27):
                exit()
