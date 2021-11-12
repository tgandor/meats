#!/usr/bin/env python

import argparse

import cv2

parser = argparse.ArgumentParser()
parser.add_argument("mask")
parser.add_argument("files", nargs="+")
parser.add_argument(
    "--augument", "-a", type=int, default=7, help="mask augumentation radius"
)
parser.add_argument(
    "--algorithm", "-A", type=int, default=1, help="Algo ID, 0: NS; 1: TELEA"
)
parser.add_argument("--save", "-w", action="store_true")
parser.add_argument("--show-orig", action="store_true")
parser.add_argument("--show-mask", action="store_true")
parser.add_argument(
    "--delay", "-d", type=int, default=0, help="cv2.waitKey() delay [ms]"
)

args = parser.parse_args()

mask = cv2.imread(args.mask, cv2.IMREAD_GRAYSCALE)
shape = (args.augument, args.augument)
mask2 = cv2.morphologyEx(
    mask, cv2.MORPH_DILATE, cv2.getStructuringElement(cv2.MORPH_RECT, shape)
)

for frame_file in args.files:
    frame = cv2.imread(frame_file)
    new_frame = cv2.inpaint(frame, mask2, 3, args.algorithm)
    if args.save:
        cv2.imwrite(frame_file, new_frame)
    else:
        if args.show_orig:
            cv2.imshow("orig", frame)
        if args.show_mask:
            cv2.imshow("mask", mask2)
        cv2.imshow("frame", new_frame)
        key = cv2.waitKey(args.delay)
        if key & 0xff == ord('q'):
            break
