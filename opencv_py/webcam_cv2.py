#!/usr/bin/env python

# from http://docs.opencv.org/
# no PIL, pygame or anything.

import numpy as np
import cv2
import sys



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
    # other
    global fullscreen
    # params
    kernel = 9
    min_kernel = 3
    max_kernel = 25
    # effect flags
    grayscale = False
    gaussian = False
    mean = False
    median = False
    # other
    fullscreen = False
reset()

if len(sys.argv) > 1:
    device = int(sys.argv[1])
else:
    device = 0

cap = cv2.VideoCapture(device)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
first_frame = True

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print('Error grabbing.')
        break

    # Our operations on the frame come here

    if grayscale:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if gaussian:
        frame = cv2.GaussianBlur(frame, (kernel, kernel), 0)

    if mean:
        frame = cv2.blur(frame, (kernel, kernel))

    if median:
        frame = cv2.medianBlur(frame, kernel)

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
