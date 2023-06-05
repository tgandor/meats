#!/usr/bin/env python

import argparse
import multiprocessing
import os

import cv2
from skimage.metrics import structural_similarity


def calculate_ssim(image1, image2):
    img1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)

    score, _ = structural_similarity(img1, img2, full=True)
    return float(score)


def ssim(t):
    return t + (calculate_ssim(*t),)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate SSIM values for consecutive image pairs"
    )
    parser.add_argument("files", nargs="+", help="Image files to calculate SSIM")
    parser.add_argument("--threshold", "-t", type=float, default=1.01)
    parser.add_argument("--delete", "-d", action="store_true")
    args = parser.parse_args()

    p = multiprocessing.Pool()
    copies = []

    for image1, image2, ssim_value in p.imap(ssim, zip(args.files, args.files[1:])):
        if ssim_value < args.threshold:
            print(f"SSIM value between {image1} and {image2}: {ssim_value}")
        else:
            copies.append(image2)

    if args.delete:
        for image in copies:
            os.remove(image)


if __name__ == "__main__":
    main()
