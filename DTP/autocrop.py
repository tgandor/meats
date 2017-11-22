#!/usr/bin/env python

import cv2
import glob
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('paths', nargs='+', help='Files to autocrop')
parser.add_argument('--overwrite', '-w', action='store_true', help='Save cropped files over original')
parser.add_argument('--step', '-s', type=int, help='Try to cut off as many rows/cols at a time', default=10)
args = parser.parse_args()

for path in args.paths:
    for filename in glob.glob(path):
        img = cv2.imread(filename)
        print(filename)
        prev = 1
        results = []
        for i in range(img.shape[0] // args.step // 2):
            avg = np.average(img[args.step*i:, ...])
            absolute = avg - prev
            relative = avg / prev
            print(i*args.step, 'average', avg, 'absolute', absolute, 'relative', relative)
            results.append((avg, i * args.step))
        best = max(results)
        print('best:', best)
        # cv2.namedWindow('crop', cv2.WINDOW_NORMAL)
        cv2.imshow('crop', img[best[1]:, ...])
        if cv2.waitKey(0) & 0xff == ord('q'):
            break
        print('-' * 60)
