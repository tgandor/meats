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
    from natsort import natsorted
except ImportError:
    natsorted = sorted

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x: x
    tqdm.write = print


def mse(img1, img2):
    return np.average((img1 - img2) ** 2)


def mouse_info(*args):
    print('Mouse callback:', args)


def _get_color(class_idx):
    class_idx += 1
    return (255 * (class_idx // 4), 255 * (class_idx // 2 % 2), 255 * (class_idx % 2))


def _scale_rect(x, y, w, h, W, H):
    x, y, w, h = list(map(float, [x, y, w, h]))
    pt1 = tuple(map(int, ((x-w/2)*W, (y-h/2)*H)))
    pt2 = tuple(map(int, ((x+w/2)*W, (y+h/2)*H)))
    return pt1, pt2


def _load_image(filename, args=None):
    image = cv2.imread(filename)

    if image is None:
        return

    if args and args.yolo_bbox:
        bbox_filename = os.path.splitext(filename)[0]+'.txt'
        H, W = image.shape[:2]
        try:
            with open(bbox_filename) as bbox:
                for line in bbox:
                    class_idx, x, y, w, h = line.split()
                    class_idx = int(class_idx)
                    pt1, pt2 = _scale_rect(x, y, w, h, W, H)
                    cv2.rectangle(image, pt1, pt2, _get_color(class_idx), 1)
        except OSError:
            tqdm.write('Failed to load: {} (bounding boxes)'.format(bbox_filename))
    return image


def quick_view_directory(directory_name, args=None):
    quit = ord('q')
    data = natsorted(glob.glob(directory_name + '/*.*'))
    prev = None
    pause = False
    for filename in tqdm(sorted(data)):
        try:
            image = _load_image(filename, args)
            if image is None:
                tqdm.write('Failed to load: {}'.format(filename))
                continue
        except cv2.error:
            tqdm.write('Error loading: {}'.format(filename))
            continue

        if prev is not None and args and args.mse > 0.:
            current_mse = mse(prev, image)
            if current_mse < args.mse:
                if args and args.delete_other:
                    os.unlink(filename)
                continue
            if args.verbose:
                tqdm.write('Showing: {} (MSE: {})'.format(filename, current_mse))
            prev = image
        else:
            prev = image

        cv2.imshow(directory_name, image)
        res = cv2.waitKey(args.delay if args else 1)

        # pause
        if pause or res & 0xff == 32:
            while True:
                res = cv2.waitKey(100)
                if res & 0xff == 32:
                    pause = False
                    break
                elif res & 0xff == ord('.'):
                    pause = True
                    break

        if res & 0xff == quit:
            return True


def view_file(filename, args=None):
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    image = _load_image(filename, args)
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
    parser.add_argument('--yolo-bbox', action='store_true', help='try to load and draw YOLO boundinb boxes')
    parser.add_argument('--verbose', '-v', action='store_true', help='increase verbosity')
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    quit = False
    for name in args.files:
        if os.path.isfile(name):
            quit = view_file(name, args)
        elif os.path.isdir(name):
            quit = quick_view_directory(name, args)
        else:
            print('WARNING: argument ignored: {}'.format(name))
        if quit:
            break
