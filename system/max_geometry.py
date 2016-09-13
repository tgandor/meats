#!/usr/bin/env python

import os
import re
import sys


if __name__ == '__main__':
    xrandr_output = os.popen('xrandr').readlines()
    if len([l for l in xrandr_output if 'connected' in l]) == 1:
        print('-f')
        exit()
    x = 0
    y = 2160
    for l in (l for l in xrandr_output if '*' in l):
        w, h = list(map(int, re.findall('\s+(\d+)x(\d+)', l)[0]))
        # print(w, h)
        x += w
        y = min(y, h)

    print('-g {}x{}'.format(x, y))
