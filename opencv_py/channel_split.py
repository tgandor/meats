#!/usr/bin/env python

import cv2
import numpy as np
import os
import sys

SHOW = True
SAVE = False


def split_channels(filename):
    img = cv2.imread(filename)
    if len(img.shape) != 3 or img.shape[2] != 3:
        sys.stderr.write('{0}: not a correct color image'.format(filename))
        return
    channels = cv2.split(img)
    zero_channel = np.zeros_like(channels[0])
    red_img = cv2.merge([zero_channel, zero_channel, channels[2]])
    green_img = cv2.merge([zero_channel, channels[1], zero_channel])
    blue_img = cv2.merge([channels[0], zero_channel, zero_channel])
    if SHOW:
        cv2.imshow('Red channel', red_img)
        cv2.imshow('Green channel', green_img)
        cv2.imshow('Blue channel', blue_img)
        cv2.waitKey(0)
    if SAVE:
        name, extension = os.path.splitext(filename)
        cv2.imwrite(name+'_red'+extension, red_img)
        cv2.imwrite(name+'_green'+extension, green_img)
        cv2.imwrite(name+'_blue'+extension, blue_img)


def main():
    if len(sys.argv) < 2:
        print('Usage: {0} <rgb_image>...'.format(sys.argv[0]))
    map(split_channels, sys.argv[1:])


if __name__ == '__main__':
    main()