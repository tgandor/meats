#!/usr/bin/env python

# from http://docs.opencv.org/
# no PIL, pygame or anything.

import cv2

# BGR, so blue = 0, green = 1, red = 2
channel = 2

cap = cv2.VideoCapture(0)

ret, prev_frame = cap.read()
prev_red = prev_frame[:, :, channel].copy()

while ret:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # colored = frame + prev_frame
    # colored = cv2.add(frame, prev_frame)

    # We need the copy, to be able to convert to cvMat down below...
    red_channel = frame[:, :, channel].copy()
    double = cv2.add(red_channel, red_channel)
    colored = cv2.resize(double, (2*640, 2*480))
    prev_red = red_channel

    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('colored', colored)

    prev_frame = frame
    in_key = cv2.waitKey(1) & 0xFF
    if in_key == ord('q'):
        break
    elif in_key == ord('n'):
        channel = (channel + 1) % 3
        print('Next channel:', channel)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
