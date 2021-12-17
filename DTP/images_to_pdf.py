#!/usr/bin/env python

from __future__ import print_function

import argparse
import glob
import os
import sys

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader

margin_x = 0 * cm  # horizontal; margins are on both sides
margin_y = 0 * cm  # includes footer
footer_y = 2 * cm  # where page numbers go


def update_settings():
    global margin_x, margin_y, footer_y
    if os.getenv("MX"):
        margin_x = float(os.getenv("MX")) * cm
    if os.getenv("MY"):
        margin_y = float(os.getenv("MY")) * cm
        footer_y = margin_y - 1 * cm


def create_image_pdf(images, args):
    c = canvas.Canvas(args.output)

    format = A4
    if args.landscape:
        c.setPageSize(landscape(A4))
        format = landscape(A4)

    if args.title:
        c.setTitle(args.title)

    num_pages = len(images)
    for filename in images:
        image = ImageReader(filename)
        img_w, img_h = image.getSize()
        avail_w = format[0] - 2 * args.margin_x * cm
        avail_h = format[1] - 2 * args.margin_y * cm
        scale = min(avail_w / img_w, avail_h / img_h)
        target_w = img_w * scale
        target_h = img_h * scale
        target_x = args.margin_x * cm + (
            0 if args.no_center else (avail_w - target_w) / 2
        )
        target_y = args.margin_y * cm + (
            0 if args.no_center else (avail_h - target_h) / 2
        )
        c.drawImage(image, target_x, target_y, target_w, target_h)
        page_num = c.getPageNumber()
        if not args.no_footer:
            text = (
                str(page_num)
                if args.no_total
                else "{0} / {1:d}".format(page_num, num_pages)
            )
            c.drawCentredString(A4[0] / 2, args.footer_y * cm, text)
        c.showPage()
        print("Processed {} - page {}".format(filename, page_num))
    c.save()
    if sys.platform.startswith("linux"):
        os.system('xdg-open "%s"' % args.output)
    else:
        os.system('start "" "%s"' % args.output)


def get_files(image_files):
    try:
        from natsort import natsorted as sort_function
    except ImportError:
        print("Warning: missing natsort")
        sort_function = sorted

    for path in image_files:
        if os.path.isfile(path):
            yield path
        elif "*" in path or "[" in path:
            # yield from glob.glob(path)
            for image in sort_function(glob.glob(path)):
                yield image
        else:
            print("Path not found:", path, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o", help="Output PDF file", default="images.pdf")
    parser.add_argument(
        "--margin-x",
        help="Left and right margin in cm",
        type=float,
        default=margin_x / cm,
    )
    parser.add_argument(
        "--margin-y",
        help="Top and bottom margin in cm",
        type=float,
        default=margin_y / cm,
    )
    parser.add_argument(
        "--footer-y",
        help="Footer offset from bottom",
        type=float,
        default=footer_y / cm,
    )
    parser.add_argument(
        "--no-total", "-n", help="Suppress total page count", action="store_true"
    )
    parser.add_argument(
        "--no-footer",
        "-N",
        help="Suppress page numbers altogether",
        action="store_true",
    )
    parser.add_argument(
        "--landscape", "-w", action="store_true", help="Use landscape orientation"
    )
    parser.add_argument(
        "--no-center", action="store_true", help="No centering on page, just margins"
    )
    parser.add_argument("--title", help="PDF title")
    parser.add_argument("image_files", nargs="+", help="Input images")
    args = parser.parse_args()
    images = list(get_files(args.image_files))
    create_image_pdf(images, args)


if __name__ == "__main__":
    update_settings()
    main()
