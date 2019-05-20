#!/usr/bin/env python

from __future__ import print_function

# Acknowledgements:
# https://realpython.com/face-recognition-with-python/
# https://github.com/shantnu/FaceDetect/

import os
import time

import cv2

MAX_SLOUCH_RATIO = 0.2  # relative to img height

initial_face_position = None
is_slouching = False

cap = cv2.VideoCapture(0)

# Create the haar cascade
cascades = [
    '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml',
    'haarcascade_frontalface_default.xml',
]

if hasattr(cv2, 'data'):
    cascades.insert(0, os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))

for path in cascades:
    if os.path.isfile(path):
        print('Loading face model:', path)
        faceCascade = cv2.CascadeClassifier(path)
        break
else:
    print('No haarcascade_frontalface_default.xml found.')
    print('Try:\nsudo apt install opencv-data\nor:')
    print('wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml')
    exit()


def face_area(rect):
    "Ugly hack, because Py3 can't unpack tuples in lambda."
    x, y, w, h = rect
    del x, y
    return w * h


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print('Error grabbing')
        exit()

    h, w = frame.shape[:2]

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )

    if len(faces) == 0:
        print(time.strftime('%H:%M:%S'), 'No faces found')
    else:
        # pick biggest face (a bit heuristic)
        x, y, w, h = max(faces, key=face_area)

        if initial_face_position is None:
            initial_face_position = y + h//2
            print(time.strftime('%H:%M:%S'), 'Noted initial face middle:', initial_face_position)
        elif (y + h//2) - initial_face_position > MAX_SLOUCH_RATIO * h:
            is_slouching = True
            print('{} STOP SLOUCHING! (Face middle {}, from initial {})'.format(time.strftime('%H:%M:%S'), y, initial_face_position))
        elif is_slouching:
            print(time.strftime('%H:%M:%S'), 'Back to normal')
            is_slouching = False

        # Draw a rectangle around the faces
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
