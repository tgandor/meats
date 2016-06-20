#!/usr/bin/env python

import os
import sys

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

margin_x = 2*cm  # horizontal; margins are on both sides
margin_y = 3*cm  # includes footer
footer_y = 2*cm  # where page numbers go


def update_settings():
    global margin_x, margin_y, footer_y
    if os.getenv('MX'):
        margin_x = float(os.getenv('MX')) * cm
    if os.getenv('MY'):
        margin_y = float(os.getenv('MY')) * cm
        footer_y = margin_y - 1*cm


def create_image_pdf(images, output="images.pdf"):
    c = canvas.Canvas(output)
    num_pages = len(images)
    for filename in images:
        image = ImageReader(filename)
        img_w, img_h = image.getSize()
        avail_w = A4[0] - 2 * margin_x
        avail_h = A4[1] - 2 * margin_y
        scale = min(avail_w/img_w, avail_h/img_h)
        target_w = img_w * scale
        target_h = img_h * scale
        target_x = margin_x + (avail_w - target_w) / 2
        target_y = margin_y + (avail_h - target_h) / 2
        c.drawImage(image, target_x, target_y, target_w, target_h)
        page_num = c.getPageNumber()
        text = '{0} / {1:d}'.format(page_num, num_pages)
        c.drawCentredString(A4[0] / 2, footer_y, text)
        c.showPage()
        print('Processed {} - page {}'.format(filename, page_num))
    c.save()
    if sys.platform.startswith('linux'):
        os.system('xdg-open "%s"' % output)
    else:
        os.system('start "" "%s"' % output)


def main():
    if len(sys.argv) < 2:
        print('Usage: {} [-o OUTPUT.pdf] IMAGE_FILE...'.format(sys.argv[0]))
        exit()
    else:
        images = sys.argv[1:]
        if '-o' in images:
            idx = images.index('-o')
            output = images.pop(idx+1)
            images.pop(idx)
            create_image_pdf(images, output)
        else:
            create_image_pdf(images)


if __name__ == "__main__":
    update_settings()
    main()
