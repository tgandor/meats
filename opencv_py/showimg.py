#!/usr/bin/env python

from __future__ import print_function

import argparse
import glob
import os
import sys
import time

import cv2
import numpy as np

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x: x
    tqdm.write = print


def mse(img1, img2):
    return np.average((img1 - img2) ** 2)


def mouse_info(*args):
    print('Mouse callback:', args)


def quick_view_directory(directory_name, min_mse=0., delay=1, verbose=True, delete_other=False):
    quit = ord('q')
    data = glob.glob(directory_name + '/*.*')
    prev = None
    for filename in tqdm(sorted(data)):
        try:
            image = cv2.imread(filename)
            if image is None:
                tqdm.write('Failed to load: {}'.format(filename))
                continue
        except cv2.error:
            tqdm.write('Error loading: {}'.format(filename))
            continue

        if prev is not None and min_mse > 0.:
            current_mse = mse(prev, image)
            if current_mse < min_mse:
                if delete_other:
                    os.unlink(filename)
                continue
            if verbose:
                tqdm.write('Showing: {} (MSE: {})'.format(filename, current_mse))
            prev = image
        else:
            prev = image

        cv2.imshow(directory_name, image)
        res = cv2.waitKey(delay)

        # pause
        if res & 0xff == 32:
            while True:
                res = cv2.waitKey(delay)
                if res & 0xff == 32:
                    break

        if res & 0xff == quit:
            return True


def view_file(filename):
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    image = cv2.imread(filename)
    cv2.imshow('image', image)
    cv2.resizeWindow('image', image.shape[1], image.shape[0])
    cv2.setMouseCallback('image', mouse_info)

    while True:
        res = cv2.waitKey(0)
        print('You pressed %d (0x%x), LSB: %d (%s)' % (
            res, res, res % 256,
            repr(chr(res % 256)) if res % 256 < 128 else '?'
        ))
        if res % 256 in [27, ord('q')]:
            return True
        elif res % 256 == 32:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mse', type=float, help='min MSE between images in directory to display', default=0)
    parser.add_argument('--delay', type=int, help='miliseconds to wait beween directory images', default=1)
    parser.add_argument('--delete-similar', action='store_true', help='remove directory images below MSE')
    parser.add_argument('--verbose', '-v', action='store_true', help='increase verbosity')
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    quit = False
    for name in args.files:
        if os.path.isfile(name):
            quit = view_file(name)
        elif os.path.isdir(name):
            quit = quick_view_directory(name, args.mse, args.delay, args.verbose, args.delete_similar)
        else:
            print('WARNING: argument ignored: {}'.format(name))
        if quit:
            break
