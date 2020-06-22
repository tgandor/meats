#!/usr/bin/env python

from __future__ import print_function, division

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
    global max_info_mode
    # effect flags
    global grayscale
    global gaussian
    global mean
    global median
    global mirror
    # other
    global fullscreen
    global info
    global info_mode
    global record
    # params
    kernel = 9
    min_kernel = 3
    max_kernel = 25
    max_info_mode = 1
    # effect flags
    grayscale = False
    gaussian = False
    mean = False
    median = False
    mirror = False
    # other
    fullscreen = False
    info = False
    info_mode = 0
    record = False


reset()

parser = argparse.ArgumentParser()
parser.add_argument('--fps', '-fps', type=float, help='FPS to set on the video capture')
parser.add_argument('--width', '-W', type=int)
parser.add_argument('--height', '-H', type=int)
parser.add_argument('--fourcc', help='Set FourCC for video source (hack)')
parser.add_argument('--delay', '-s', type=float, help='Time to sleep between frames (seconds)')
parser.add_argument('--frame', type=int, help='Starting frame to (try to) skip to.', default=0)
parser.add_argument('device', type=str, nargs='?',
                    help='device number, video file name or network stream URL', default='0')
args = parser.parse_args()

device = int(args.device) if re.match(r'\d+$', args.device) else args.device

cap = cv2.VideoCapture(device)
if args.width:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
if args.height:
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)


initial_fps = cap.get(cv2.CAP_PROP_FPS)
print('Opened with FPS:', initial_fps)
print('Frame count:', cap.get(cv2.CAP_PROP_FRAME_COUNT))
initial_fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
print('FourCC:', [chr(((initial_fourcc >> (8*i)) & 0xff)) for i in range(4)] if initial_fourcc else '0')
print('Format:', cap.get(cv2.CAP_PROP_FORMAT))
print('Width:', cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('Height:', cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print('Frame Count:', cap.get(cv2.CAP_PROP_FRAME_COUNT))
print('Frame Pos:', cap.get(cv2.CAP_PROP_POS_FRAMES))

if args.frame:
    cap.set(cv2.CAP_PROP_POS_FRAMES, args.frame)
    print('New Frame Pos:', cap.get(cv2.CAP_PROP_POS_FRAMES))

if args.fps:
    cap.set(cv2.CAP_PROP_FPS, args.fps)
    prop_fps = cap.get(cv2.CAP_PROP_FPS)
    print('After setting to', args.fps, 'we get', prop_fps)
else:
    prop_fps = initial_fps

if args.fourcc:
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*args.fourcc))
    print('After setting FourCC:', cap.get(cv2.CAP_PROP_FOURCC))

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
first_frame = True
frame_idx = 0
start_time = time.time()
total_saved = 0

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
        if info_mode == 0:
            message = 'Frame {}, ~fps: {:.2f}, {}'.format(frame_idx, fps, frame.shape)
        elif info_mode == 1:
            message = time.strftime('%Y-%m-%d %H:%M:%S, frame: ') + str(frame_idx)
        else:
            message = 'Mode not supported ;)'

        # sometimes this assignment is not necessary:
        frame = cv2.putText(frame,
            message,
            (0, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,  # font scale
            (0, 255, 255),  # yellow
            2  # thickness
        )

    if record:
        filename = time.strftime('%Y%m%d_%H%M%S_') + str(frame_idx) + '.jpg'
        cv2.imwrite(filename, frame)
        size = os.path.getsize(filename)
        total_saved += size
        rate = int(total_saved * 3600 // (time.time() - start_time))
        print('frame saved: {}, {:,} KB, {:,} MB total, ~ {:,} MB/h'.format(
            filename, size // 2**10, total_saved // 2**20, rate // 2**20))

    # Display the resulting frame
    if all(dim > 0 for dim in frame.shape):
        cv2.imshow('frame', frame)
    else:
        print('Empty frame!')
        continue

    if first_frame:
        cv2.resizeWindow('frame', frame.shape[1], frame.shape[0])
        first_frame = False

    raw_key = cv2.waitKey(int(args.delay * 1000 + 0.5) if args.delay else 1)
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
    elif key == ord('I'):
        info_mode = info_mode + 1 if info_mode < max_info_mode else 0
    elif key == ord('l'):
        # mirror, as in 'looking glass'
        mirror = not mirror
    elif key == ord('m'):
        mean = not mean
    elif key == ord('M'):
        median = not median
    elif key == ord('h'):
        print('''Key bindings:
    h - print key bindings
    r - reset settings
    b - toggle grayscale
    i - toggle info OSD
    I - cycle through OSD modes
    l - mirror (flip vertically) 'looking glass'
    m - mean filter
    M - median filter
    s - save jpg screenshot
    S - save png screenshot
    v - toggle 'record video' - i.e. screenshot every frame to:
        time.strftime('%Y%m%d_%H%M%S_') + str(frame_idx) + '.jpg'
    / - original size (resize window; only for CV_WINDOW_NORMAL)

    Space - pause
    q - quit
    ''')
    elif key in (ord('s'), ord('S')):
        filename = time.strftime('%Y%m%d_%H%M%S') + ('.jpg' if key == ord('s') else '.png')
        cv2.imwrite(filename, frame)
        print('Screenshot saved:', os.path.abspath(filename))
    elif key == ord('v'):
        record = not record
        print('Recoding:', record)
    elif key == ord('/'):
        cv2.resizeWindow('frame', frame.shape[1], frame.shape[0])
    elif key == ord('-'):
        kernel = max(kernel-2, min_kernel)
    elif key == ord('+') or key == ord('='):
        kernel = min(kernel+2, max_kernel)
    elif key == ord(' '):
        # pause
        print('Paused at frame:', frame_idx)
        if 0 < prop_fps < 120:
            print('Approximate time [seconds]:', frame_idx / prop_fps)
        while True:
            key = cv2.waitKey(1000) & 0xFF
            if key == ord(' '):
                break
            elif key == ord('q'):
                exit()
    elif raw_key not in (-1, 0xff):
        print('Unhandled key: {k}, 0x{k:x}, {char}, raw: {r}'.format(k=key, r=raw_key, char=repr(chr(key))))

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
