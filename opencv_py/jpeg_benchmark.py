#!/usr/bin/env python

import argparse
import sys
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt
import tqdm

# this is (being) deprecated:
# from skimage.measure import compare_ssim as ssim, compare_mse as mse
from skimage.metrics import structural_similarity as ssim, mean_squared_error as mse

timer = time.clock if sys.version_info < (3,) else time.perf_counter


def partial_sums(x, kernel_size=8):
    """Calculate partial sums of array in boxes (kernel_size x kernel_size).

    This corresponds to:
    scipy.signal.convolve2d(x, np.ones((kernel_size, kernel_size)), mode='valid')
    >>> partial_sums(np.arange(12).reshape(3, 4), 2)
    array([[10, 14, 18],
           [26, 30, 34]])
    """
    assert len(x.shape) >= 2 and x.shape[0] >= kernel_size and x.shape[1] >= kernel_size
    sums = x.cumsum(axis=0).cumsum(axis=1)
    sums = np.pad(sums, 1)[:-1, :-1]
    return (
        sums[kernel_size:, kernel_size:]
        + sums[:-kernel_size, :-kernel_size]
        - sums[:-kernel_size, kernel_size:]
        - sums[kernel_size:, :-kernel_size]
    )


def universal_image_quality_index(x, y, kernel_size=8):
    """Compute the Universal Image Quality Index (UIQI) of x and y."""

    N = kernel_size ** 2

    x = x.astype(np.float)
    y = y.astype(np.float)
    e = np.finfo(np.float).eps

    # sums and auxiliary expressions based on sums
    S_x = partial_sums(x, kernel_size)
    S_y = partial_sums(y, kernel_size)
    PS_xy = S_x * S_y
    SSS_xy = S_x*S_x + S_y*S_y

    # sums of squares and product
    S_xx = partial_sums(x*x, kernel_size)
    S_yy = partial_sums(y*y, kernel_size)
    S_xy = partial_sums(x*y, kernel_size)

    num = 4 * PS_xy * (N * S_xy - PS_xy)
    den = (N*(S_xx + S_yy) - SSS_xy) * (SSS_xy)

    Q_s = (num) / (den + e)

    return np.mean(Q_s)


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

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('--downsample', type=int)
args = parser.parse_args()

filename = args.file

orig_image = cv2.imread(filename, cv2.IMREAD_COLOR)

if args.downsample:
    orig_image = orig_image[::args.downsample, ::args.downsample]

sizes = []
mses = []
ssims = []
uiqis = []
compression_times = []
decompression_times = []

print('UIQI(x, x) = ', universal_image_quality_index(orig_image, orig_image))
print('SSIM(x, x) = ', ssim(orig_image, orig_image, multichannel=True))

for quality in tqdm.trange(101):
    data, image, time_c, time_d = check_compression(orig_image, quality)
    ssims.append(ssim(orig_image, image, multichannel=True))
    sizes.append(len(data))
    mses.append(mse(image, orig_image))
    uiqis.append(universal_image_quality_index(image, orig_image))
    compression_times.append(time_c)
    decompression_times.append(time_d)

size1 = len(check_lossless_compression(image, 1))
size9 = len(check_lossless_compression(image, 9))
print('PNG compression range:', size9, size1)

size = image.nbytes

fig = plt.figure(filename + ' JPEG performance')

ax = fig.add_subplot(2, 2, 1)
ax.set_title('Size ratio (blue) and Structural Similarity Index (orange)')
plt.plot(np.array(sizes) / size)
plt.axhline(size1 / size, color='red')
plt.axhline(size9 / size, color='green')
plt.plot(ssims, color='orange')
plt.plot(uiqis, color='magenta')

ax = fig.add_subplot(2, 2, 2)
ax.set_title('Mean Squared Error')
plt.plot(mses)

ax = fig.add_subplot(2, 2, 3)
ax.set_title('Compression (blue) vs decompression (orange) time')
plt.plot(compression_times, color='blue')
plt.plot(decompression_times, color='orange')

ax = fig.add_subplot(2, 2, 4)
ax.imshow(cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB))

plt.show()

# Bibliography

# https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
# SSIM, Wang et al.: https://www.cns.nyu.edu/pub/eero/wang03-reprint.pdf (2004)
# "Image Quality Assessment: From Error Visibility to Structural Similarity"
# Google Scholar seems to not find it for "SSIM" query.
# https://scikit-image.org/docs/dev/api/skimage.metrics.html#skimage.metrics.structural_similarity
# https://scikit-image.org/docs/dev/api/skimage.metrics.html#skimage.metrics.mean_squared_error
