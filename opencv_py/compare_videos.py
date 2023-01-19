#!/usr/bin/env python

import argparse
import multiprocessing as mp
import os

import cv2
import numpy as np


def capture_to_queue(queue: mp.JoinableQueue, source):
    cap = cv2.VideoCapture(source)
    while True:
        ret, frame = cap.read()
        queue.put((ret, frame))


class MPCapture:
    def __init__(self, source) -> None:
        self.source = source
        self.queue = mp.JoinableQueue()
        self.process = mp.Process(target=capture_to_queue, args=(self.queue, source))
        self.process.start()

    def read(self):
        return self.queue.get()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v3", action="store_true", help="compare 3-way")
    parser.add_argument(
        "--full", action="store_true", help="display full filenames in window title"
    )
    parser.add_argument(
        "--delay", type=int, help="wait between frames [ms]. 0 = forever", default=40
    )
    parser.add_argument(
        "--vcrop", "-H", type=int, help="crop frames to H lines of image"
    )
    parser.add_argument(
        "--hcrop", "-W", type=int, help="crop frames to W columns of image"
    )
    parser.add_argument(
        "--separate", "-s", action="store_true", help="use separate windows to preview"
    )
    parser.add_argument(
        "--multiprocess",
        "-m",
        action="store_true",
        help="use separate processes to capture",
    )
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()

    paths = args.files

    if not paths:
        paths = [input("Video path {}: ".format(i)) for i in range(3 if args.v3 else 2)]

    if args.multiprocess:
        readers = [MPCapture(path) for path in paths]
    else:
        readers = [cv2.VideoCapture(path) for path in paths]

    names = paths if args.full else map(os.path.basename, paths)
    window = " vs ".join(names)

    if not args.separate:
        cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    else:
        for name in names:
            cv2.namedWindow(name, cv2.WINDOW_NORMAL)

    pause = False

    while True:
        rets_frames = [cap.read() for cap in readers]

        if not all(ret for ret, _ in rets_frames):
            print("Some streams failed to read next frame.")
            import code

            code.interact(local=locals())
            break

        frames = [frame for _, frame in rets_frames]

        if args.hcrop:
            frames = [frame[:, : args.hcrop] for frame in frames]

        if args.vcrop:
            frames = [frame[: args.vcrop] for frame in frames]

        if not args.separate:
            assert (
                len({frame.shape[0] for frame in frames}) == 1
            ), "Frame heights must be equal"
            tiles = np.hstack(frames)
            cv2.imshow(window, tiles)
        else:
            for name, frame in zip(names, frames):
                cv2.imshow(name, frame)

        ret = cv2.waitKey(args.delay)

        if ret & 0xFF in (ord("q"), 27):
            break

        elif ret & 0xFF == ord(" ") or ret & 0xFF == ord(".") or pause:
            pause = True
            while True:
                ret = cv2.waitKey(1000)
                if ret & 0xFF == ord(" "):
                    pause = False
                    break
                if ret & 0xFF == ord("."):
                    break
                if ret & 0xFF in (ord("q"), 27):
                    exit()


if __name__ == "__main__":
    main()
