#!/usr/bin/env python

from __future__ import print_function

import glob
import os
import sys
import time

import cv2

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x: x


def mouse_info(*args):
    print('Mouse callback:', args)


def quick_view_directory(name):
    quit = ord('q')
    data = glob.glob(name+'/*.*')
    N = len(data)
    start = time.time()
    for filename in tqdm(sorted(data)):
        image = cv2.imread(filename)
        cv2.imshow(name, image)
        res = cv2.waitKey(1)
        if res & 0xff == quit:
            break


if len(sys.argv) < 2:
    print('Usage: {0} <image_file>'.format(sys.argv[0]))
    exit()

name = sys.argv[1]
cv2.namedWindow(name, cv2.WINDOW_NORMAL)

if os.path.isdir(name):
    quick_view_directory(name)
    exit()


image = cv2.imread(name)
cv2.imshow(name, image)
cv2.resizeWindow(name, image.shape[1], image.shape[0])
cv2.setMouseCallback(name, mouse_info)

while True:
    res = cv2.waitKey(0)
    print('You pressed %d (0x%x), LSB: %d (%s)' % (
        res, res, res % 256,
        repr(chr(res%256)) if res%256 < 128 else '?'
    ))
    if res % 256 in [27, 32, ord('q')]:
        break
