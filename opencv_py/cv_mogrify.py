#!/usr/bin/env python

import cv2
import sys

if len(sys.argv) < 2:
    print('Usage: {0} <command> <image_file>'.format(sys.argv[0]))
    exit()

command = sys.argv[1]
target = sys.argv[2]

if command == 'otsu':
    image = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
    value, result = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print('Determined threshold value: {0}'.format(value))
    cv2.imwrite(target, result)
else:
    print('Error. Unknown command: {0}'.format(command))
