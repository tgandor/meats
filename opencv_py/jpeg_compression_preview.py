#!/usr/bin/env python

import sys

import cv2

DEFAULT_QUALITY = 95
WINDOW_FLAGS = cv2.WINDOW_AUTOSIZE  # (too) large window for large image
WINDOW_FLAGS = cv2.WINDOW_GUI_NORMAL  # nice, auto scales... same as WINDOW_NORMAL?
WINDOW_FLAGS = cv2.WINDOW_KEEPRATIO  # looks like other flags also keep the ratio...
WINDOW_FLAGS = cv2.WINDOW_NORMAL

def update_quality(value):
    global orig_image
    data = cv2.imencode('.jpg', orig_image, [cv2.IMWRITE_JPEG_QUALITY, value])[1]
    print('Quality: {}, data size: {:,}'.format(value, len(data)))
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cv2.imshow('jpeg_preview', image)


orig_image = cv2.imread(sys.argv[1])
cv2.namedWindow('jpeg_preview', WINDOW_FLAGS)
cv2.createTrackbar('Q', 'jpeg_preview', DEFAULT_QUALITY, 100, update_quality)
update_quality(DEFAULT_QUALITY)

while True:
    key = cv2.waitKey(10) & 0xff
    # print(key)
    if key in (27, ord('q')):
        break
