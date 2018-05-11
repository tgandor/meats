#!/usr/bin/env python

import argparse
import cv2
import glob
import os
import re
import time

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--skip", help="initial frames to skip", default=0, type=int)
parser.add_argument("-f", "--format", help="file format (extension) to use", default="jpg")
parser.add_argument("-t", "--timestamp", help="initial frames to skip", action="store_true")
parser.add_argument("videos", help="videos to extract frame from", nargs='*')
args = parser.parse_args()


def videos(videos_args):
    """Generate VideoCapture source values based on arguments."""

    if not videos_args:
        yield 0  # default webcam
        return

    for arg in videos_args:
        if '*' in arg or '?' in arg:
            for file_name in glob.glob(arg):
                yield file_name
        elif re.match(r'\d+$', arg):
            yield int(arg)
        else:
            yield arg


for source in videos(args.videos):
    cap = None
    try:
        cap = cv2.VideoCapture(source)
        for _ in range(args.skip):
            cap.read()
        status, frame = cap.read()
        if not status:
            raise RuntimeError('Error reading frame')
        file_name = ''
        if args.timestamp:
            file_name += time.strftime('%Y%m%d_%H%M%S_')
        source_basename = os.path.splitext(str(source))[0]
        file_name += source_basename + '.' + args.format
        cv2.imwrite(file_name, frame)
        print('Source: {} - Saved frame to: {}'.format(source, file_name))
    finally:
        if cap:
            cap.release()
