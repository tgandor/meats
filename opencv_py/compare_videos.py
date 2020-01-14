import argparse
import os

import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-v3', action='store_true', help='compare 3-way')
args = parser.parse_args()

paths = [
    input('Video path {}: '.format(i))
    for i in range(3 if args.v3 else 2)
]

readers = [cv2.VideoCapture(path) for path in paths]

window = ' vs '.join(map(os.path.basename, paths))

cv2.namedWindow(window, cv2.WINDOW_NORMAL)

while True:
    rets_frames = [cap.read() for cap in readers]

    if not all(ret for ret, _ in rets_frames):
        print('Some streams failed to read next frame.')
        break

    frames = [frame for _, frame in rets_frames]

    assert len({frame.shape for frame in frames}) == 1, 'Frame shapes must be equal'

    tiles = np.hstack(frames)

    cv2.imshow(window, tiles)
    ret = cv2.waitKey(40)

    if ret & 0xff == ord('q'):
        break

    elif ret & 0xff == ord(' '):
        while True:
            ret = cv2.waitKey(1000)
            if ret & 0xff == ord(' '):
                break
