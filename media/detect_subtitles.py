#!/usr/bin/env python

import argparse
import glob
import os

import cv2
import numpy as np
import tqdm


def inpaint_subtible(frame_file, shape, radius, algorithm):
    frame = cv2.imread(frame_file)
    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mask = np.zeros_like(frame_bw)
    cv2.threshold(frame_bw, 230, 255, cv2.THRESH_BINARY, mask)
    mask[: 4 * mask.shape[0] // 5] = 0  # leave bottom 20%
    mask2 = cv2.morphologyEx(
        mask, cv2.MORPH_DILATE, cv2.getStructuringElement(cv2.MORPH_RECT, shape)
    )
    new_frame = cv2.inpaint(frame, mask2, radius, algorithm)
    cv2.imwrite(frame_file, new_frame)

def _get_pattern(args):
    pattern = args.files_glob
    if os.path.isdir(pattern):
        pattern += '/*'
    return pattern


def _parallel_inpaint(args):
    # https://stackoverflow.com/a/59905309/1338797
    from tqdm.contrib.concurrent import process_map
    from functools import partial

    mapper = partial(
        inpaint_subtible,
        shape=(args.augument, args.augument),
        radius=args.radius,
        algorithm=args.algorithm,
    )

    pattern = _get_pattern(args)
    files = sorted(glob.glob(pattern))

    process_map(mapper, files, chunksize=32)


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files_glob", help="glob expression for input files")
    parser.add_argument(
        "--delay", "-d", type=int, default=0, help="cv2.waitKey() delay [ms]"
    )
    parser.add_argument("--inpaint", "-I", action="store_true")
    parser.add_argument(
        "--augument", "-a", type=int, default=9, help="mask augumentation radius"
    )
    parser.add_argument(
        "--algorithm", "-A", type=int, default=1, help="inpaint algo: 0=NS, 1=TELEA"
    )
    parser.add_argument(
        "--radius", "-r", type=int, default=4, help="inpaint neighborhood radius"
    )
    parser.add_argument("--save", "-w", action="store_true")
    parser.add_argument("--parallel", "-p", action="store_true")
    args = parser.parse_args()

    if args.parallel:
        _parallel_inpaint(args)
        return

    shape = (args.augument, args.augument)

    pattern = _get_pattern(args)
    for frame_file in tqdm.tqdm(sorted(glob.glob(pattern))):
        frame = cv2.imread(frame_file)
        frame_bw = cv2.imread(frame_file, cv2.IMREAD_GRAYSCALE)

        mask = np.zeros_like(frame_bw)
        cv2.threshold(frame_bw, 230, 255, cv2.THRESH_BINARY, mask)
        mask[: 4 * mask.shape[0] // 5] = 0  # leave bottom 20%

        if not args.save:
            cv2.imshow("mask", mask)
            cv2.imshow("frame", frame)

        if args.inpaint:
            mask2 = cv2.morphologyEx(
                mask, cv2.MORPH_DILATE, cv2.getStructuringElement(cv2.MORPH_RECT, shape)
            )
            new_frame = cv2.inpaint(frame, mask2, args.radius, args.algorithm)

            if args.save:
                cv2.imwrite(frame_file, new_frame)
                continue

            cv2.imshow("inpaint", new_frame)

        key = cv2.waitKey(args.delay)
        if key & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    _main()
