#!/usr/bin/env python

import argparse
import itertools as it
import os

import cv2
from matplotlib.pyplot import axis


def bounding_box(img):
    def sum_ax(img, ax):
        if len(img.shape) == 3:
            return img.sum(axis=(ax, 2))
        return img.sum(axis=ax)

    def num_zeros(arr):
        val, g = next(it.groupby(arr))
        if val != 0:
            return 0
        return len(list(g))

    def pre_post(sums):
        inv = sums.max() - sums
        return num_zeros(inv), num_zeros(inv[::-1])

    return pre_post(sum_ax(img, 0)) + pre_post(sum_ax(img, 1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("--show", "-s", action="store_true")
    parser.add_argument("--outdir", "-o")
    args = parser.parse_args()

    for path in args.files:
        img = cv2.imread(path)
        bbox = bounding_box(img)
        x0, x1, y0, y1 = bbox
        h, w = img.shape[:2]
        print(path, bbox, (x0, y0), (w - x1, h - y1))
        if args.show or args.outdir:
            cv2.rectangle(img, (x0, y0), (w - x1, h - y1), (255, 0, 0), 2)
            cv2.rectangle(img, (0, 0), (w, h), (0, 0, 255), 2)

        if args.show:
            cv2.imshow(path, img)
            cv2.waitKey(0)

        if args.outdir:
            out = os.path.join(args.outdir, path)
            cv2.imwrite(out, img)


if __name__ == "__main__":
    main()
