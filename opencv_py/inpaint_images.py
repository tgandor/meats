#!/usr/bin/env python

import argparse
import os

import cv2

parser = argparse.ArgumentParser()
parser.add_argument("mask")
parser.add_argument("files", nargs="+")
args = parser.parse_args()

mask = cv2.imread(args.mask, cv2.IMREAD_GRAYSCALE)
mask2 = cv2.morphologyEx(
    mask, cv2.MORPH_DILATE, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
)

for frame_file in args.files:
    frame = cv2.imread(frame_file)
    new_frame = cv2.inpaint(frame, mask2, 3, cv2.INPAINT_TELEA)
    cv2.imshow('frame', new_frame)
    cv2.imshow('orig', frame)
    cv2.waitKey(0)
