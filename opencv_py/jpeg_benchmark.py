#!/usr/bin/env python

import sys
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt
import tqdm

from skimage.measure import structural_similarity as ssim, mean_squared_error as mse


timer = time.clock if sys.version_info < (3,) else time.perf_counter

def check_compression(image, quality):
    start = timer()
    data = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, quality])[1]
    compressed = timer()
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    decompressed = timer()
    return data, image, compressed - start, decompressed - compressed


def check_lossless_compression(image, level):
    data = cv2.imencode('.png', image, [cv2.IMWRITE_PNG_COMPRESSION, level])[1]
    return data


filename = sys.argv[1]

orig_image = cv2.imread(filename, cv2.IMREAD_COLOR)

sizes = []
mses = []
ssims = []
compression_times = []
decompression_times = []


for quality in tqdm.trange(101):
    data, image, time_c, time_d = check_compression(orig_image, quality)
    ssims.append(ssim(orig_image, image, multichannel=True))
    sizes.append(len(data))
    mses.append(mse(image, orig_image))
    compression_times.append(time_c)
    decompression_times.append(time_d)

size1 = len(check_lossless_compression(image, 1))
size9 = len(check_lossless_compression(image, 9))
print('PNG compression range:', size9, size1)

size = image.nbytes

fig = plt.figure(filename + ' JPEG performance')

ax = fig.add_subplot(1, 3, 1)
ax.set_title('Size ratio and Structural Similarity Index')
plt.plot(np.array(sizes) / size)
plt.axhline(size1 / size, color='red')
plt.axhline(size9 / size, color='green')
plt.plot(ssims, color='orange')

ax = fig.add_subplot(1, 3, 2)
ax.set_title('Mean Squared Error')
plt.plot(mses)

ax = fig.add_subplot(1, 3, 3)
ax.set_title('Compression (blue) vs decompression (orange) time')
plt.plot(compression_times, color='blue')
plt.plot(decompression_times, color='orange')

plt.show()

# Bibliography

# https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
# SSIM, Wang et al.: https://www.cns.nyu.edu/pub/eero/wang03-reprint.pdf (2004)
# "Image Quality Assessment: From Error Visibility to Structural Similarity"
# Google Scholar seems to not find it for "SSIM" query.
# https://scikit-image.org/docs/dev/api/skimage.metrics.html#skimage.metrics.structural_similarity
# https://scikit-image.org/docs/dev/api/skimage.metrics.html#skimage.metrics.mean_squared_error
