#!/usr/bin/env python

import argparse
import multiprocessing

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
    args = parser.parse_args()

    p = multiprocessing.Pool()

    for image1, image2, ssim_value in p.imap(ssim, zip(args.files, args.files[1:])):
        print(f"SSIM value between {image1} and {image2}: {ssim_value}")


if __name__ == "__main__":
    main()
