import argparse
import os

import cv2

parser = argparse.ArgumentParser()
parser.add_argument("image")
parser.add_argument("--radius", "-r", type=int, default=15)
parser.add_argument("--cvalue", "-c", type=int, default=15)
parser.add_argument("--erode", type=int)
parser.add_argument("--close", type=int)
parser.add_argument("--suffix", default="_t", help="Name suffix for saved result.")
args = parser.parse_args()

image = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)

block = 2 * args.radius + 1 # must be an odd number
result = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block, args.cvalue)


if args.close:
    r = args.close
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r, r))
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)

if args.erode:
    r = args.erode
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r, r))
    result = cv2.morphologyEx(result, cv2.MORPH_ERODE, kernel)

cv2.imshow('Adaptive Threshold', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

base, ext = os.path.splitext(args.image)
output = base + args.suffix + ".png"
cv2.imwrite(output, result)
print("Saved to:", output)