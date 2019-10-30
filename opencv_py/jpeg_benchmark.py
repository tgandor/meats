#!/usr/bin/env python

import sys
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt
import tqdm

from skimage.measure import structural_similarity as ssim, mean_squared_error as mse


def check_compression(image, quality):
    data = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, quality])[1]
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data, image


def check_lossless_compression(image, level):
    data = cv2.imencode('.png', image, [cv2.IMWRITE_PNG_COMPRESSION, level])[1]
    return data


filename = sys.argv[1]

orig_image = cv2.imread(filename, cv2.IMREAD_COLOR)

sizes = []
mses = []
ssims = []

# TODO: compression times, de~ ~, MSE, PSNR, SSIM, % original, % raw ...

for quality in tqdm.trange(101):
    data, image = check_compression(orig_image, quality)
    ssims.append(ssim(orig_image, image, multichannel=True))
    sizes.append(len(data))
    mses.append(mse(image, orig_image))

size1 = len(check_lossless_compression(image, 1))
size9 = len(check_lossless_compression(image, 9))
print('PNG compression range:', size9, size1)

size = image.nbytes

fig = plt.figure(filename + ' JPEG performance')
ax = fig.add_subplot(1, 2, 1)
ax.set_title('Size ratio and Structural Similarity Index')
plt.plot(np.array(sizes) / size)
plt.axhline(size1 / size, color='red')
plt.axhline(size9 / size, color='green')
plt.plot(ssims, color='orange')
ax = fig.add_subplot(1, 2, 2)
ax.set_title('Mean Squared Error')
plt.plot(mses)

plt.show()

# Bibliography

# https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
# SSIM, Wang et al.: https://www.cns.nyu.edu/pub/eero/wang03-reprint.pdf (2004)
# Google Scholar seems to not find it for "SSIM" query.
