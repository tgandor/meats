#!/usr/bin/env python

from __future__ import print_function

import argparse
import glob
import os
import random
import time

import cv2


def create_detector():
    # Create the haar cascade
    cascades = [
        '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml',
        'haarcascade_frontalface_default.xml',
    ]

    if hasattr(cv2, 'data'):
        cascades.insert(0, os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))

    for path in cascades:
        if os.path.isfile(path):
            print('Loading face model:', path)
            faceCascade = cv2.CascadeClassifier(path)
            break
    else:
        print('No haarcascade_frontalface_default.xml found.')
        print('Try:\nsudo apt install opencv-data\nor:')
        print('wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml')
        exit()

    return faceCascade


parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--inverse', '-v', action='store_true', help='print or show where no faces found')
parser.add_argument('--show', action='store_true')
parser.add_argument('--show-all', '-a', action='store_true')
parser.add_argument('--delay', type=int, default=100, help='only used with --show')
parser.add_argument('--progress', action='store_true')
parser.add_argument('--shuffle', action='store_true')

args = parser.parse_args()
faceCascade = create_detector()

fast = args.delay < 500

files = [
    result
    for pattern in args.files
    for result in glob.glob(pattern)
]

if args.shuffle:
    random.shuffle(files)

if args.progress:
    try:
        from tqdm import tqdm
        show = tqdm.write
    except ImportError:
        tqdm = lambda x: x
        show = print
else:
    tqdm = lambda x: x
    show = print

for result in tqdm(files):
    image = cv2.imread(result, cv2.IMREAD_GRAYSCALE)
    # Detect faces in the image

    faces = faceCascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )

    if (len(faces) == 0) == args.inverse:
        show(result)

    if args.show:
        if not args.show_all and (len(faces) == 0) != args.inverse:
            continue

        for x, y, w, h in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), 255, 2)

        # name for high delay, generic for fast viewing

        if fast:
            cv2.namedWindow('face detection', cv2.WINDOW_NORMAL)
            cv2.imshow('face detection', image)
        else:
            cv2.namedWindow(result, cv2.WINDOW_NORMAL)
            cv2.imshow(result, image)

        res = cv2.waitKey(args.delay) & 0xff

        if not fast:
            cv2.destroyAllWindows()

        if res == ord('q'):
            break

        if res == ord(' '):
            while cv2.waitKey() == -1:
                pass

cv2.destroyAllWindows()
