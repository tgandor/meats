#!/usr/bin/env python

import argparse
import cv2
import time

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="output file (include '%d' for number sequence)", default='cam_%d.jpg')
parser.add_argument("-d", "--device", help="increase output verbosity", default=0, type=int)
parser.add_argument("-p", "--delay", help="delay period between captures", default=1, type=float)
parser.add_argument("-q", "--quiet", help="print less messages", action='store_true')
parser.add_argument("-n", "--count", help="frame capture limit", default=-1, type=int)
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


avg_period = Average()

prev_frame = None
same_frames = 0
same_frames_max = 1

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        counter += 1
        now = time.time()
        avg_period.sample(now - then)
        then = now

        if args.delay <= 0 or now >= next_capture:
            if args.timestamp:
                cv2.putText(frame,
                            time.strftime("%Y-%m-%d %H:%M:%S") + ' {:.1f} fps'.format(1/avg_period.get()),
                            (0, 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0)
                )
            frame_counter += 1
            output = args.output % (frame_counter,) if '%' in args.output else args.output
            cv2.imwrite(output, frame)
            if not args.quiet:
                print('Stored frame {} (input frame {}) to {}'.format(frame_counter, counter, output))
            next_capture = now + args.delay
            if frame_counter == args.count:
                break

        if prev_frame is not None and (frame == prev_frame).all():
            print('Same frame again')
            same_frames += 1
            if same_frames >= same_frames_max:
                print('Max same frames ({}) reached, exiting.'.format(same_frames_max))
                break
        else:
            same_frames = 0

        prev_frame = frame

finally:
    cap.release()
