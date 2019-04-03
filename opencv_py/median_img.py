#!/usr/bin/env python

# https://stackoverflow.com/questions/28682985/temporal-median-image-of-multiple-images

from __future__ import print_function

import argparse
import glob
import itertools

import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('glob_or_filenames', nargs='+')
parser.add_argument('--save', '-o', help='filename to save result')


args = parser.parse_args()

images = []

for filename in itertools.chain.from_iterable(map(glob.glob, args.glob_or_filenames)):
    image = cv2.imread(filename)  # TODO: read always 3-channel?
    print('Stacking', filename, image.shape)
    images.append(image)

# The final cast (to uint8) - makes all the difference
# else OpenCV seems to expect 0.0 - 1.0 values when displaying.

# print('Shape before median:', np.shape(images))
median_image = np.median(images, axis=0).astype(np.uint8)
# print('Shape after median:', median_image.shape)

# print(images)
# print(median_image)

if args.save:
    cv2.imwrite(args.save, median_image)
else:
    cv2.imshow('orig', images[0])
    cv2.imshow('median', median_image)
    cv2.waitKey(0)
