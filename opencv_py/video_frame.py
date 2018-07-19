#!/usr/bin/env python

import argparse
import cv2
import glob
import os
import re
import time

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--skip", help="initial frames to skip", default=0, type=int)
parser.add_argument("-n", "--count", help="frames to save", default=1, type=int)
parser.add_argument("-f", "--format", help="file format (extension) to use", default="jpg")
parser.add_argument("-t", "--timestamp", help="prepend timestamp to filename", action="store_true")
parser.add_argument("videos", help="videos to extract frame from", nargs='*')
args = parser.parse_args()


def videos(videos_args):
    """Generate VideoCapture source values based on arguments."""

    if not videos_args:
        yield 0  # default webcam
        return

    for arg in videos_args:
        if '*' in arg:
            for file_name in glob.glob(arg):
                yield file_name
        elif re.match(r'\d+$', arg):
            yield int(arg)
        else:
            yield arg


def _slugify(string):
    kill_chars = '/?$#:&'
    consider = kill_chars + '_., =+@'
    return ''.join(('_' if c in kill_chars else c) for c in string if c.isalnum() or c in consider)


def source_to_filename(source_or_url):
    if isinstance(source_or_url, int):
        return 'video{}'.format(source_or_url)

    if source_or_url.startswith('rtsp://') or source_or_url.startswith('http://'):
        clean = _slugify(source_or_url)
        print('Old: {}\nNew: {}'.format(source_or_url, clean))
        return clean

    return os.path.splitext(str(source))[0]


for source in videos(args.videos):
    cap = None
    frame = None

    try:
        print('Opening video: {}'.format(source))
        cap = cv2.VideoCapture(source)

        for _ in range(args.skip):
            status, frame = cap.read()
            if not status:
                raise RuntimeError('Error reading frame')

        for i in range(args.count):
            status, frame = cap.read()
            if not status:
                raise RuntimeError('Error reading frame')

            file_name = ''

            if args.timestamp:
                file_name += time.strftime('%Y%m%d_%H%M%S_')

            file_name += source_to_filename(source)

            if args.count > 1:
                file_name += '_{:03d}'.format(i)

            file_name += '.' + args.format
            cv2.imwrite(file_name, frame)
            print('Source: {} - Saved frame to: {}'.format(source, file_name))
    finally:
        if cap:
            cap.release()
