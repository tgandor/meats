#!/usr/bin/env python

import sys
import time

import cv2

import matplotlib.pyplot as plt


def check_compression(image, quality):
    time.clock()
    data = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, quality])[1]
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data, image


orig_image = cv2.imread(sys.argv[1])

sizes = []

# TODO: compression times, de~ ~, MSE, PSNR, SSIM, % original, % raw ...

for quality in range(101):
    data, image = check_compression(orig_image, quality)

    sizes.append(len(data))

plt.plot(sizes)
plt.show()
