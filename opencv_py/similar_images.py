#!/usr/bin/env python

import argparse
import multiprocessing

import cv2
from skimage.metrics import structural_similarity as ssim


def calculate_ssim(image1, image2):
    img1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)

    score, _ = ssim(img1, img2, full=True)
    return score


def main():
    parser = argparse.ArgumentParser(
        description="Calculate SSIM values for consecutive image pairs"
    )
    parser.add_argument("files", nargs="+", help="Image files to calculate SSIM")
    args = parser.parse_args()

    p = multiprocessing.Pool()

    for image1, image2 in p.imap(
        lambda t: calculate_ssim(*t), zip(args.files, args.files[1:])
    ):
        ssim_value = calculate_ssim(image1, image2)
        print(f"SSIM value between {image1} and {image2}: {ssim_value}")


if __name__ == "__main__":
    main()
