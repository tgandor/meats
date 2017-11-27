#!/usr/bin/env python

import cv2
import glob
import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('paths', nargs='+', help='Files to autocrop')
parser.add_argument('--overwrite', '-w', action='store_true', help='Save cropped files over original')
parser.add_argument('--preview', '-v', action='store_true', help='Show cv2 preview of cropped image')
parser.add_argument('--step', '-s', type=int, help='Try to cut off as many rows/cols at a time', default=10)

args = parser.parse_args()


def crop_by_average(img):
    def make_slices(array):
        return slice(*array[:2]), slice(*array[2:])

    def pick_best(slices, delta):
        print('by delta', delta)
        if sum(delta) > 0:
            hot_idx = np.argmax(delta)
            tries = (slices[hot_idx+1] - slices[hot_idx]) // 4 // delta[hot_idx]
        else:
            hot_idx = np.argmin(delta)
            tries = (slices[hot_idx-1] - slices[hot_idx]) // 4 // delta[hot_idx]

        results = []
        for i in range(tries):
            h_slice, w_slice = make_slices(slices)
            avg = np.average(img[h_slice, w_slice, ...])
            print(slices, avg)
            results.append((avg, slices.copy()))
            slices += delta
        best = max(results)
        print('best:', best)
        return best[1]

    slices_orig = np.array([0, img.shape[0], 0, img.shape[1]])

    slices = np.diag([
        pick_best(slices_orig, np.array([args.step, 0, 0, 0])),
        pick_best(slices_orig, np.array([0, -args.step, 0, 0])),
        pick_best(slices_orig, np.array([0, 0, args.step, 0])),
        pick_best(slices_orig, np.array([0, 0, 0, -args.step]))
    ])

    return img[make_slices(slices)]


for path in args.paths:
    for filename in glob.glob(path):
        img = cv2.imread(filename)
        print(filename)
        img_cropped = crop_by_average(img)
        if args.preview:
            cv2.imshow('crop', img_cropped[::2, ::2])
            if cv2.waitKey(0) & 0xff == ord('q'):
                break
        target = filename if args.overwrite else 'crop_' + filename
        cv2.imwrite(target, img_cropped)

        print('-' * 60)
