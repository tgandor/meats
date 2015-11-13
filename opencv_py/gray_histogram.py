#!/usr/bin/env python

import cv2
import pylab as pl
import sys

img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
n, bins, patches = pl.hist(img.flat, bins=pl.np.arange(257))
pl.gcf().canvas.set_window_title(sys.argv[1] + ' - Gray Histogram')
pl.show()
