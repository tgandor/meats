#!/usr/bin/env python

import numpy as np
import math
import cv2
import sys

from fractions import Fraction


def cv_size(img):
    return tuple(img.shape[1::-1])


def get_screen_res():
    if sys.platform.startswith('linux'):
        import os
        lines = [line for line in os.popen('xrandr').read().split('\n') if line.find('*') != -1]
        return tuple(map(int, lines[0].split()[0].split('x')))
    else:
        return 800, 600

SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_res()


def show_fit(img, name='preview', expand=False, rotate=False):
    w, h = cv_size(img)
    W, H = SCREEN_WIDTH, SCREEN_HEIGHT
    if w <= W and h <= H and not expand:
        to_show = img
    elif w > W or h > H:
        if rotate and min(Fraction(W, w), Fraction(H, h)) < min(Fraction(W, h), Fraction(H, w)):
            img = cv2.flip(cv2.transpose(img), 0)
            w, h = h, w
        if h * W > H * w:
            w1 = w * H / h
            h1 = H
        else:
            w1 = W
            h1 = h * W / w
        to_show = cv2.resize(img, (w1, h1))
    else:  # expand ...
        raise NotImplementedError
    cv2.imshow(name, to_show)


def main():
    img = cv2.imread(sys.argv[1])
    print cv_size(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, region = cv2.threshold(img, 128.0, 255.0, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, rho=1, theta=math.pi/180.0, threshold=80, minLineLength=60, maxLineGap=10)
    print lines
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    show_fit(img, rotate=True)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()
