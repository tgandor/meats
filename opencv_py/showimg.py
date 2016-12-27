#!/usr/bin/env python

from __future__ import print_function

import cv2
import sys


def mouse_info(*args):
    print('Mouse callback:', args)

if len(sys.argv) < 2:
    print('Usage: {0} <image_file>'.format(sys.argv[0]))
    exit()


name = sys.argv[1]
cv2.namedWindow(name, cv2.WINDOW_NORMAL)
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
