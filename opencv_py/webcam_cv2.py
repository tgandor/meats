#!/usr/bin/env python

from __future__ import print_function

"""
Script to show a webcam or a video file and overlay simple effects.

from http://docs.opencv.org/
no PIL, pygame or anything.
"""

import argparse
import numpy as np
import cv2
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

if len(sys.argv) > 1:
    device = sys.argv[1]
    if re.match(r'\d+$', device):
        # int for webcam capture, string -> video filename
        device = int(sys.argv[1])
else:
    device = 0

cap = cv2.VideoCapture(device)

if len(sys.argv) > 2:
    fps = int(sys.argv[2])
    cap.set(cv2.CAP_PROP_FPS, fps)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
first_frame = True
frame_idx = 0
start_time = time.time()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret and False:
        print('Error grabbing.')
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
        message = 'Frame {}, ~fps: {:.2f}'.format(frame_idx, fps)
        cv2.putText(frame,
            message,
            (0, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,  # font scale
            (0, 255, 255),  # yellow
            2  # thickness
        )

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if first_frame:
        cv2.resizeWindow('frame', frame.shape[1], frame.shape[0])
        first_frame = False

    key = cv2.waitKey(1) & 0xFF
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

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
