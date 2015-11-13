#!/usr/bin/env python

import cv2
import pylab as pl
import sys

img = cv2.imread(sys.argv[1], cv2.IMREAD_ANYCOLOR)

if len(img.shape) < 3:
    print('This image is 1-channel')
    exit(1)

new_shape = (img.shape[0] * img.shape[1], img.shape[2])

n, bins, patches = pl.hist(img.reshape(new_shape), bins=pl.np.arange(257), histtype='step')
pl.gcf().canvas.set_window_title(sys.argv[1] + ' - Color Histogram')
pl.show()

