#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

import os
from collections import Counter

try:
    import piexif
except ImportError:
    print('Missing piexif')
    os.system('pip install piexif')
    exit()

try:
    import imagesize
except ImportError:
    print('Missing imagesize')
    os.system('pip install imagesize')
    exit()

size_stats = Counter()
examples = {}

for path, directories, files in os.walk('.'):
    for basename in files:
        if basename.lower().endswith('.jpg'):
            realname = os.path.join(path, basename)
            d = piexif.load(realname)

            try:
                size = (d["0th"][piexif.ImageIFD.ImageWidth], d["0th"][piexif.ImageIFD.ImageLength])
            except KeyError:
                print('Error reading size from EXIF:', realname)
                size = None

            size2 = imagesize.get(realname)

            if size is None:
                size = size2

            assert size == size2

            size_stats[size] += 1
            if size not in examples:
                examples[size] = realname

total = len(size_stats)

if total == 0:
    print('No images found. Sorry.')
    exit()

ordered_keys = sorted(size_stats.keys(), key=lambda x: x[0] * x[1])

for size in ordered_keys:
    count = size_stats[size]
    print('{} {:.1f} MPix, {} files, {:.1f} %, example: {}'.format(
        size, size[0] * size[1] / 1e6, count, count / total, examples[size]))

try:
    import matplotlib.pyplot as plt
except ImportError:
    print('Missing matplotlib. No plot to show.')
    exit()

def transpose(tuples):
    return list(zip(*tuples))


w, h, n = transpose([(width, height, count) for (width, height), count in size_stats.items()])

plt.scatter(w, h, s=n)

# keep the visible aspect ratio -
# sorry, this doesn't work:
# plt.axis('equal')  # https://stackoverflow.com/a/2935000/1338797
# but this, does.
plt.axis('scaled')  # https://stackoverflow.com/a/35994245/1338797

# reset axes min to 0:
plt.xlim(left=0)
plt.ylim(bottom=0)

plt.show()
