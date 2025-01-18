#!/usr/bin/env python

import argparse
import sys

import cv2

parser = argparse.ArgumentParser()
parser.add_argument("input_video", nargs="?", default=0)
parser.add_argument("--min-area", "-m", type=int, default=500)
args = parser.parse_args()

cap = cv2.VideoCapture(args.input_video)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Create the background subtractor object using MOG2 algorithm.
back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)
# Kernel for morphological opening and dilation
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply background subtraction to get the foreground mask
    fg_mask = back_sub.apply(frame)
    # Open operation to remove noise
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    # Make more bold
    fg_mask = cv2.dilate(fg_mask, kernel, iterations=1)

    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around detected moving objects
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > args.min_area:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Frame', frame)
    cv2.imshow('Foreground Mask', fg_mask)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
