#!/usr/bin/env python

import argparse
import itertools as it
import os

import cv2
import numpy as np


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
    parser.add_argument("--center", "-c", action="store_true")
    parser.add_argument("--draw", "-d", action="store_true")
    parser.add_argument("--outdir", "-o")
    parser.add_argument("--show", "-s", action="store_true")
    parser.add_argument("--vmargin", "-v", type=int)
    args = parser.parse_args()

    v_margins = []

    for path in args.files:
        img = cv2.imread(path)
        bbox = bounding_box(img)
        x0, x1, y0, y1 = bbox
        h, w = img.shape[:2]
        print(path, bbox, (x0, y0), (w - x1, h - y1))

        if args.draw:
            cv2.rectangle(img, (x0, y0), (w - x1, h - y1), (255, 0, 0), 2)

        if args.center:
            print(f"Rolling left by {(x1-x0) // 2}")
            img = np.roll(img, (x1 - x0) // 2, axis=1)
            v_margins.append((y0 + y1) // 2)

        if args.vmargin:
            print(f"Rolling down by {args.vmargin - y0}")
            img = np.roll(img, args.vmargin - y0, axis=0)

        if args.draw:
            cv2.rectangle(img, (0, 0), (w, h), (0, 0, 255), 2)

        if args.show:
            cv2.imshow(path, img)
            if cv2.waitKey(0) & 0xFF == ord("q"):
                break

        if args.outdir:
            out = os.path.join(args.outdir, path)
            cv2.imwrite(out, img)

    if args.center:
        print(v_margins)
        print("Min V margin:", min(v_margins))


if __name__ == "__main__":
    main()
