#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

import argparse
import glob
import os

import cv2
import numpy as np

try:
    from natsort import natsorted
except ImportError:
    natsorted = sorted

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x: x
    tqdm.write = print


def mse(img1, img2):
    return np.average((img1 - img2) ** 2)


def mouse_info(*args):
    print("Mouse callback:", args)


def _get_color(class_idx):
    class_idx += 1
    return (255 * (class_idx // 4), 255 * (class_idx // 2 % 2), 255 * (class_idx % 2))


def _scale_rect(x, y, w, h, W, H):
    x, y, w, h = list(map(float, [x, y, w, h]))
    pt1 = tuple(map(int, ((x - w / 2) * W, (y - h / 2) * H)))
    pt2 = tuple(map(int, ((x + w / 2) * W, (y + h / 2) * H)))
    return pt1, pt2


# https://docs.opencv.org/3.0-beta/modules/imgcodecs/doc/reading_and_writing_images.html
ACCEPTED_EXTENSIONS = {
    ".bmp",
    ".dib",  # Windows bitmaps  (always supported)
    ".jpeg",
    ".jpg",
    ".jpe",  # JPEG files  (see the Notes section)
    ".jp2",  # JPEG 2000 files  (see the Notes section)
    ".png",  # Portable Network Graphics  (see the Notes section)
    ".webp",  # WebP  (see the Notes section)
    ".pbm",
    ".pgm",
    ".ppm",  # Portable image format  (always supported)
    ".sr",
    ".ras",  # Sun rasters  (always supported)
    ".tiff",
    ".tif",  # TIFF files  (see the Notes section)
}


def _load_image(filename, args=None):
    # leaving this to imread() lead to crashes on occasion:
    _, ext = os.path.splitext(filename)
    if ext.lower() not in ACCEPTED_EXTENSIONS:
        tqdm.write("Skipping: {} (rejected extension: {})".format(filename, ext))
        return None

    if args.glymur and ext.lower() == ".jp2":
        # https://glymur.readthedocs.io/en/latest/how_do_i.html#read-images
        import glymur

        jp2 = glymur.Jp2k(filename)
        # of course, glymur has normal color channels:
        image = cv2.cvtColor(jp2[:], cv2.COLOR_RGB2BGR)
    else:
        image = cv2.imread(filename)

    if image is None:
        tqdm.write("Failed to load: {}".format(filename))
        return None

    if args and args.rot180:
        # this is (possibly) faster, but non-contiguous:
        image = np.rot90(image, k=2)
        # this is also nice, and gives a contiguous array right away:
        # image = cv2.rotate(image, cv2.ROTATE_180)

    if args and args.yolo_bbox:
        bbox_filename = os.path.splitext(filename)[0] + ".txt"
        H, W = image.shape[:2]
        image = np.ascontiguousarray(image)
        try:
            with open(bbox_filename) as bbox:
                for line in bbox:
                    class_idx, x, y, w, h = line.split()
                    class_idx = int(class_idx)
                    pt1, pt2 = _scale_rect(x, y, w, h, W, H)
                    thickness = max(args.downsample, 1)
                    cv2.rectangle(image, pt1, pt2, _get_color(class_idx), thickness)
        except OSError:
            tqdm.write("Failed to load: {} (bounding boxes)".format(bbox_filename))

    if args and args.chessboard:
        wh = args.chessboard.split(",")
        if len(wh) == 2:
            w, h = map(int, wh)
            ret, corners = cv2.findChessboardCorners(image, (w, h), None)
            if not ret:
                print("Corners not found")
            else:
                print("Found corners:", corners.shape)
                # drawing corners needs to have a contiguous array
                image = np.ascontiguousarray(image)
                cv2.drawChessboardCorners(image, (w, h), corners, ret)

    if args and args.downsample > 1:
        return image[:: args.downsample, :: args.downsample]

    return image


def quick_view_directory(directory_name, args=None):
    quit = ord("q")
    data = natsorted(glob.glob(directory_name + "/*.*"))
    prev = None
    pause = False
    for filename in tqdm(sorted(data)):
        try:
            image = _load_image(filename, args)
            if image is None:
                continue
        except cv2.error:
            tqdm.write("Error loading: {}".format(filename))
            continue

        if prev is not None and args and args.mse > 0.0:
            current_mse = mse(prev, image)
            if current_mse < args.mse:
                if args and args.delete_similar:
                    os.unlink(filename)
                continue
            if args.verbose:
                tqdm.write("Showing: {} (MSE: {})".format(filename, current_mse))
            prev = image
        else:
            prev = image

        cv2.imshow(directory_name, image)
        res = cv2.waitKey(args.delay if args else 1)

        # pause
        if pause or res & 0xFF == 32:
            while True:
                res = cv2.waitKey(100)
                if res & 0xFF == 32:
                    pause = False
                    break
                elif res & 0xFF == ord("."):
                    pause = True
                    break

        if res & 0xFF == quit:
            return True


def fhd_fit(image):
    w, h = 1920, 1080
    hi, wi = image.shape[:2]

    if hi > h or wi > w:
        down_scale = max(wi / w, hi / h)
        hi, wi = [int(x / down_scale) for x in (hi, wi)]

    cv2.resizeWindow("image", (wi, hi))


def view_file(filename, args=None):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    image = _load_image(filename, args)

    if image is None:
        return

    window = filename if args.title else "image"
    cv2.imshow(window, image)

    if args and args.fit:
        fhd_fit(image)

    cv2.setMouseCallback(window, mouse_info)

    while True:
        res = cv2.waitKey(0)
        print(
            "You pressed %d (0x%x), LSB: %d (%s)"
            % (res, res, res % 256, repr(chr(res % 256)) if res % 256 < 128 else "?")
        )
        if res % 256 in (27, ord("q"), ord("x")):
            return True
        elif res % 256 in (32, 13):
            break
        elif res % 256 == ord("c"):
            print("cls")
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chessboard", help="chesboard size to detect and show")
    parser.add_argument(
        "--delay",
        type=int,
        help="miliseconds to wait beween directory images",
        default=1,
    )
    parser.add_argument(
        "--downsample",
        type=int,
        help="display image downsampled N times (stride)",
        default=1,
    )
    parser.add_argument(
        "--fit",
        "-f",
        action="store_true",
        help="resize window to 1080p (can help on some backends)",
    )
    parser.add_argument(
        "--glymur",
        action="store_true",
        help="use glymur library to load .jp2 images (OpenJPEG, no JasPer)",
    )
    parser.add_argument(
        "--mse",
        type=float,
        help="min MSE between images in directory to display",
        default=0,
    )
    parser.add_argument(
        "--rot180", action="store_true", help="rotate image 180 degrees"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="increase verbosity"
    )
    parser.add_argument(
        "--yolo-bbox",
        action="store_true",
        help="try to load and draw YOLO boundinb boxes",
    )
    parser.add_argument("--title", action="store_true", help="use titles for images")
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    quit = False
    for name in args.files:
        if os.path.isfile(name):
            quit = view_file(name, args)
        elif os.path.isdir(name):
            quit = quick_view_directory(name, args)
        elif "**" in name:
            # it's not 2020 yet, being nice to Py2
            for path in glob.glob(name, recursive=True):
                print(name, "->", path)
                quit = view_file(path, args)
                if quit:
                    break
        elif "*" in name:
            for path in glob.glob(name):
                print(name, "->", path)
                quit = view_file(path, args)
                if quit:
                    break
        else:
            print("WARNING: argument ignored: {}".format(name))
        if quit:
            break
