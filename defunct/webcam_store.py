#!/usr/bin/env python

import argparse
import cv2
import numpy
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="output file (include '%%d' for number sequence)", default='cam_%d.jpg')
parser.add_argument("-d", "--device", help="increase output verbosity", default=0, type=int)
parser.add_argument("-p", "--delay", help="delay period between captures", default=0, type=float)
parser.add_argument("-q", "--quiet", help="print less messages", action='store_true')
parser.add_argument("-n", "--count", help="frame capture limit", default=-1, type=int)
parser.add_argument("-s", "--skip", help="initial frames to skip", default=1, type=int)
parser.add_argument("-t", "--timestamp", help="add timestamp to image", action='store_true')
args = parser.parse_args()

cap = cv2.VideoCapture(args.device)

counter = 0
frame_counter = 0
next_capture = then = time.time()


class Average:
    def __init__(self):
        self.sum = 0
        self.count = 0

    def sample(self, val):
        self.sum += val
        self.count += 1

    def get(self):
        if not self.count:
            return None
        return self.sum / self.count


class Namer:
    def __init__(self, pattern):
        self.pattern = pattern
        self.counter = 0
        self.number = 0
        self.last_name = None

    def get_name(self):
        self.counter += 1

        if '%' not in self.pattern:
            return self.pattern

        self.number += 1
        if os.path.exists(self.pattern % self.number):
            self._find_free_number()

        self.last_name = self.pattern % self.number
        return self.last_name

    def _find_free_number(self):
        left = right = self.number

        while os.path.exists(self.pattern % right):
            right *= 2

        while left < right-1:
            middle = (left + right + 1) // 2

            if os.path.exists(self.pattern % middle):
                left = middle
            else:
                right = middle

        self.number = right


avg_period = Average()
namer = Namer(args.output)

prev_frame = None
same_frames = 0
same_frames_max = 1

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print('Capture failed.')
            break

        counter += 1
        now = time.time()
        avg_period.sample(now - then)
        then = now

        if prev_frame is not None and (frame == prev_frame).all():
            print('Same frame again')
            same_frames += 1
            if same_frames >= same_frames_max:
                print('Max same frames ({}) reached, exiting.'.format(same_frames_max))
                break
        else:
            same_frames = 0

        prev_frame = numpy.array(frame, copy=True)

        if counter > args.skip and (args.delay <= 0 or now >= next_capture):
            average = numpy.average(prev_frame)
            message = time.strftime("%Y-%m-%d %H:%M:%S") + ' {:.1f} fps'.format(1/avg_period.get())

            # TODO: does this work?
            frame[:,0:20] = numpy.divide(frame[:,0:20], 3)

            if args.timestamp:
                cv2.putText(frame,
                            message,
                            (0, 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, # font scale
                            (0, 255, 255) if average < 96 else (96, 0, 0), # color: (B, G, R) - of course
                            2 # thickness
                )

            cv2.imwrite(namer.get_name(), frame)
            if not args.quiet:
                print('Frame {} (input frame {}) stored to {} (average: {:.1f})'.format(
                    namer.counter, counter, namer.last_name, average))
            next_capture = now + args.delay
            if frame_counter == args.count:
                break

finally:
    cap.release()
