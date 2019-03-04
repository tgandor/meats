#!/usr/bin/env python

# Acknowledgements:
# https://realpython.com/face-recognition-with-python/
# https://github.com/shantnu/FaceDetect/

import os

import cv2

MAX_SLOUCH_RATIO = 0.2  # relative to img height

initial_face_position = None

cap = cv2.VideoCapture(0)

# Create the haar cascade
cascades = [
    '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml',
    'haarcascade_frontalface_default.xml',
]

for path in cascades:
    if os.path.isfile(path):
        faceCascade = cv2.CascadeClassifier(path)
        break
else:
    print('No haarcascade_frontalface_default.xml found.')
    print('Try: sudo apt install opencv-data')
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

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
        print('No faces found')
        continue
    # print("Found {0} faces!".format(len(faces)))

    # pick biggest face (a bit heuristic)
    x, y, w, h = max(faces, key=lambda (x, y, w, h): w * h)

    if initial_face_position is None:
        initial_face_position = y
    elif y - initial_face_position > MAX_SLOUCH_RATIO * h:
        print('STOP SLOUCHING! (Face top {}, from initial {})'.format(y, initial_face_position))

    # Draw a rectangle around the faces
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
