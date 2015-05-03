#!/usr/bin/env python

import cv2
import sys

if len(sys.argv) < 2:
    print('Usage: {0} <image_file>'.format(sys.argv[0]))
    exit()

cv2.imshow(sys.argv[1], cv2.imread(sys.argv[1]))

while True:
    res = cv2.waitKey(0)
    print 'You pressed %d (0x%x), LSB: %d (%s)' % (
        res, res, res % 256,
        repr(chr(res%256)) if res%256 < 128 else '?'
    )
    if res % 256 in [27, 32, ord('q')]:
        break
