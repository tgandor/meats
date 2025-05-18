#!/usr/bin/env python

"""
Script for calling tesseract with output == basename+'.txt' for each argument.

Some protection against overwriting existing files.
Update 2025-05-18: handle PDFs (multipage) with pdftoppm from poppler.
"""

import argparse
import glob
import os
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", "-l", help="Language to use")
    parser.add_argument("--debug", "-d", action="store_true")
    parser.add_argument("--polish", "-pl", action="store_true")
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("-ocr", action="store_true")
    parser.add_argument("-nn", action="store_true")
    parser.add_argument("files", nargs="+")
    parser.add_argument("remainder", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    base_command = ["tesseract"]

    if args.lang:
        base_command.extend(["-l", args.lang])
    elif args.polish:
        base_command.extend(["-l", "pol"])

    if args.compact:
        base_command.extend(["--psm", "6"])

    if args.nn:
        base_command.extend(["--oem", "1"])
    elif args.ocr:
        base_command.extend(["--oem", "0"])

    base_command.extend(args.remainder)

    for i, image_ in enumerate(args.files):
        basename, ext = os.path.splitext(image_)

        # PDF unpacking - then inner loop for pages
        if ext.lower() == ".pdf":
            subprocess.call(["pdftoppm", "-progress", "-png", image_, basename])
            images = sorted(glob.glob(basename + "-*.png"))
        else:
            images = [image_]

        for image in images:
            basename, _ = os.path.splitext(image)

            if os.path.exists(basename + ".txt"):
                print("Skipping {} - {}.txt exists.".format(image, basename))
                continue

            print("{} -> {}.txt ...".format(image, basename))

            if args.debug:
                print(base_command + [image, basename])

            subprocess.call(base_command + [image, basename])

        if i < len(args.files) - 1:
            print("---")


if __name__ == "__main__":
    main()
