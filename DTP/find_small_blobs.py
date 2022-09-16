#!/usr/bin/env python

import argparse
import os
from collections import Counter

import cv2
import numpy as np
from scipy.ndimage import label

WHITE = 255

parser = argparse.ArgumentParser()
parser.add_argument("images", nargs="+")
parser.add_argument("--max-area", "-m", type=int, help="max area (pixels) of blob to remove", default=36)
parser.add_argument("--suffix", default="_new")
parser.add_argument("--show-labeled", "-l", action="store_true")
parser.add_argument("--show-result", "-r", action="store_true")
parser.add_argument("--no-save", "-S", action="store_true")
parser
args = parser.parse_args()

for path in args.images:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    print(path, img.shape, set(img.ravel()))
    labeled, ncomponents = label(WHITE - img)  # negative: bg is black for this
    if args.show_labeled:
        import matplotlib.pyplot as plt
        plt.imshow(labeled)
        plt.show()
    print("Number of blobs:", ncomponents)
    c = Counter(labeled.ravel())
    areas = np.array([*c.values()])  # the numbers should be in order, see assert:
    assert all(areas[i] == c[i] for i in range(ncomponents+1))
    small_blobs = areas < args.max_area
    img[small_blobs[labeled]] = WHITE  # this line is the whole thing, appreciate NumPy!

    # small_blobs[labeled] gives a boolean mask, which would be computed like that:
    # mask = np.empty_like(labeled)
    # for i in range(labeled.shape[0]):
    #     for j in range(labeled.shape[1]):
    #         mask[i, j] = small_blobs[labeled[i, j]]
    # ... which of course would take forever.
    # Well, the real forever, whould rather be like:
    # mask[i, j] = (labeled == labeled[i, j]).sum() < args.max_area
    # ... the `Counter(labeled.ravel())` and `areas` does a lot.

    if args.show_result:
        cv2.imshow(path, img)
        if cv2.waitKey() & 0xff == ord('q'):
            exit()

    if args.no_save:
        continue

    base, ext = os.path.splitext(path)
    output = base + args.suffix + ext
    cv2.imwrite(output, img)
    print("Saved to:", output)
