#!/usr/bin/env python

import argparse
import cv2
import time

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="output file", default='webcam.jpg')
parser.add_argument("-d", "--device", help="increase output verbosity", default=0, type=int)
parser.add_argument("-p", "--delay", help="delay period between captures", default=1, type=float)
parser.add_argument("-q", "--quiet", help="print less messages", action='store_true')
args = parser.parse_args()

cap = cv2.VideoCapture(args.device)
counter = 0
next_capture = time.time()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    counter += 1
    if time.time() >= next_capture:
        cv2.imwrite(args.output, frame)
        if not args.quiet:
            print('Stored frame {} to {}'.format(counter, args.output))
        next_capture = time.time() + args.delay

cap.release()
