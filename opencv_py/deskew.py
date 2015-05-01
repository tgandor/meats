#!/usr/bin/env python

import math
import cv2
import sys
import os

from fractions import Fraction


def cv_size(img):
    return tuple(img.shape[1::-1])


def cv_center(img):
    w, h = cv_size(img)
    return w/2, h/2


def get_screen_res():
    if sys.platform.startswith('linux'):
        import os
        lines = [line for line in os.popen('xrandr').read().split('\n') if line.find('*') != -1]
        return tuple(map(int, lines[0].split()[0].split('x')))
    else:
        try:
            from win32gui import GetDesktopWindow, GetWindowRect
            return tuple(GetWindowRect(GetDesktopWindow())[2:])
        except ImportError:
            pass
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
        raise NotImplementedError('Cannot expand preview image')

    scale = 1.0
    while True:
        cv2.imshow(name, to_show)
        key = cv2.waitKey(0)
        char_code = key % 256
        if char_code == ord(' '):
            break
        if char_code == ord('+'):
            scale *= 2
            to_show = cv2.resize(img, (int(w1*scale), int(h1*scale)))
            continue
        if char_code == ord('-'):
            scale /= 2
            to_show = cv2.resize(img, (int(w1*scale), int(h1*scale)))
            continue
        if char_code == ord('q'):
            exit()


def process(filename):
    print('Processing {0}...'.format(filename))
    img = cv2.imread(filename)
    print(cv_size(img))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, region = cv2.threshold(img, 128.0, 255.0, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, rho=1, theta=math.pi/180.0, threshold=80, minLineLength=60, maxLineGap=10)
    n = len(lines[0])
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)
    angles = sorted([math.atan2(y2-y1, x2-x1) for x1, y1, x2, y2 in lines[0]])
    print("There's {0} lines.".format(n))
    middle_angle = angles[n / 2] * 180/math.pi
    print('The middle angle is: {0}'.format(middle_angle))
    if -5.0 < middle_angle < 5.0:
        if middle_angle > 0.125 or middle_angle < -0.125:
            img_rotated = cv2.warpAffine(
                img,
                cv2.getRotationMatrix2D(cv_center(img), middle_angle , 1.0),
                cv_size(img),
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(255, 255, 255)
            )
            file_, extension = os.path.splitext(filename)
            cv2.imwrite('_'+file_+'_'+extension, img_rotated)
        else:
            print('The angle is too small. No action taken.')
    else:
        print('The angle is too radical. No action taken.')
    # show_fit(gray, rotate=False)


def main():
    if len(sys.argv) < 2:
        print('Usage: {0} <image_with_text_file>...'.format(sys.argv[0]))
    map(process, sys.argv[1:])


if __name__ == '__main__':
    main()
