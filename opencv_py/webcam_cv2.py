#!/usr/bin/env python

from __future__ import print_function

"""
Script to show a webcam or a video file and overlay simple effects.

from http://docs.opencv.org/
no PIL, pygame or anything.
"""

import argparse
import cv2
import os
import re
import sys
import time


def reset():
    # params
    global kernel
    global min_kernel
    global max_kernel
    # effect flags
    global grayscale
    global gaussian
    global mean
    global median
    global mirror
    # other
    global fullscreen
    global info
    # params
    kernel = 9
    min_kernel = 3
    max_kernel = 25
    # effect flags
    grayscale = False
    gaussian = False
    mean = False
    median = False
    mirror = False
    # other
    fullscreen = False
    info = False


reset()

parser = argparse.ArgumentParser()
parser.add_argument('--fps', '-fps', type=float)
parser.add_argument('--fourcc', type=str, help='Set FourCC for video source (hack)')
parser.add_argument('device', type=str, nargs='?',
                    help='device number, video file name or network stream URL', default='0')
args = parser.parse_args()

device = int(args.device) if re.match(r'\d+$', args.device) else args.device

cap = cv2.VideoCapture(device)

print('Opened with FPS:', cap.get(cv2.CAP_PROP_FPS))

if args.fps:
    cap.set(cv2.CAP_PROP_FPS, args.fps)
    print('After setting to', args.fps, 'we get', cap.get(cv2.CAP_PROP_FPS))

if args.fourcc:
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*args.fourcc))

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
first_frame = True
frame_idx = 0
start_time = time.time()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret or frame is None:
        print('Error grabbing:', ret, frame)
        if type(device) != int:
            print('Probably EOF ;)')
        break

    # Our operations on the frame come here
    frame_idx += 1

    if grayscale:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if gaussian:
        frame = cv2.GaussianBlur(frame, (kernel, kernel), 0)

    if mean:
        frame = cv2.blur(frame, (kernel, kernel))

    if median:
        frame = cv2.medianBlur(frame, kernel)

    if mirror:
        frame = cv2.flip(frame, 1)

    if info:
        fps = frame_idx / (time.time() - start_time)
        message = 'Frame {}, ~fps: {:.2f}, {}'.format(frame_idx, fps, frame.shape)
        cv2.putText(frame,
            message,
            (0, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,  # font scale
            (0, 255, 255),  # yellow
            2  # thickness
        )

    # Display the resulting frame
    if all(dim > 0 for dim in frame.shape):
        cv2.imshow('frame', frame)
    else:
        print('Empty frame!')
        continue

    if first_frame:
        cv2.resizeWindow('frame', frame.shape[1], frame.shape[0])
        first_frame = False

    raw_key = cv2.waitKey(1)
    key = raw_key & 0xFF
    if key == ord('q'):
        break
    elif key == ord('f'):
        fullscreen = not fullscreen
        cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, int(fullscreen))
    elif key == ord('r'):
        reset()
    elif key == ord('b'):
        grayscale = not grayscale
    elif key == ord('g'):
        gaussian = not gaussian
    elif key == ord('i'):
        info = not info
    elif key == ord('l'):
        # mirror, as in 'looking glass'
        mirror = not mirror
    elif key == ord('m'):
        mean = not mean
    elif key == ord('M'):
        median = not median
    elif key in (ord('s'), ord('S')):
        filename = time.strftime('%Y%m%d_%H%M%S') + ('.jpg' if key == ord('s') else '.png')
        cv2.imwrite(filename, frame)
        print('Screenshot saved:', os.path.abspath(filename))
    elif key == ord('/'):
        cv2.resizeWindow('frame', frame.shape[1], frame.shape[0])
    elif key == ord('-'):
        kernel = max(kernel-2, min_kernel)
    elif key == ord('+') or key == ord('='):
        kernel = min(kernel+2, max_kernel)
    elif key == ord(' '):
        # pause
        while True:
            key = cv2.waitKey(1000) & 0xFF
            if key == ord(' '):
                break
    elif raw_key not in (-1, 0xff):
        print('Unhandled key: {k}, 0x{k:x}, {char}, raw: {r}'.format(k=key, r=raw_key, char=repr(chr(key))))

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
