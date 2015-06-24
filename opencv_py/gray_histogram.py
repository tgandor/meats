#!/usr/bin/env python

import cv2
import pylab as P
import sys

img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
n, bins, patches = P.hist(img.flatten(), bins=P.np.arange(257))
P.show()
