#!/usr/bin/env python

import argparse
import glob
import os
import sys

import numpy as np
import cv2


def split_channels(filename, show=True, save=False):
    img = cv2.imread(filename)
    if len(img.shape) != 3 or img.shape[2] != 3:
        sys.stderr.write('{0}: not a correct color image'.format(filename))
        return
    channels = cv2.split(img)
    zero_channel = np.zeros_like(channels[0])
    red_img = cv2.merge([zero_channel, zero_channel, channels[2]])
    green_img = cv2.merge([zero_channel, channels[1], zero_channel])
    blue_img = cv2.merge([channels[0], zero_channel, zero_channel])
    if show:
        cv2.imshow('Red channel', red_img)
        cv2.imshow('Green channel', green_img)
        cv2.imshow('Blue channel', blue_img)
        cv2.waitKey(0)
    if save:
        name, extension = os.path.splitext(filename)
        cv2.imwrite(name+'_red'+extension, red_img)
        cv2.imwrite(name+'_green'+extension, green_img)
        cv2.imwrite(name+'_blue'+extension, blue_img)


def main(args):
    for filename in args.files:
        split_channels(filename, not args.no_show, args.save)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--save', '-s', action='store_true', help='save channels as separate files')
    parser.add_argument('--no-show', '-q', action='store_true', help='skip displaying results (useful for --save)')
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    main(args)
