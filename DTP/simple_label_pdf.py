#!/usr/bin/env python

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime
import os
import tempfile
import sys

font_size = 16
default_width = 20*cm
default_height = 10*cm
default_output_file = os.path.join(tempfile.gettempdir(), 'simple_label_output.pdf')
fonts_to_try = ['Ubuntu-L', 'Verdana', 'Arial']


def _setup_canvas(outfile=default_output_file):
    for font_name in fonts_to_try:
        try:
            font = TTFont(font_name, font_name+'.ttf')
            pdfmetrics.registerFont(font)
            font_to_use = font_name
            break
        except:
            font_to_use = None

    c = canvas.Canvas(outfile)
    if font_to_use:
        c.setFont(font_to_use, font_size)
    c.setTitle(outfile)
    return c


def label(c, text, width=default_width, height=default_height):
    c.saveState()
    c.setDash(2, 8)
    inv = lambda x: A4[1]-x
    c.setLineWidth(0.25)
    c.line(0, inv(height), width, inv(height))
    c.line(width, inv(0), width, inv(height))
    c.drawCentredString(width/2, inv((height+font_size)/2), text)
    c.setFontSize(12)
    c.drawCentredString(width/2, inv(height)+.5*cm, datetime.datetime.now().strftime('%Y-%m-%d (%a) %H:%M'))
    c.restoreState()


def main():
    custom = raw_input('Enter label text: ') or '.' * 30
    in_width = raw_input('Width (%.1f): ' % (default_width/cm))
    in_height = raw_input('Height (%.1f): ' % (default_height/cm))
    width = float(in_width)*cm if in_width else default_width
    height = float(in_height)*cm if in_height else default_height
    c = _setup_canvas()
    label(c, custom, width, height)
    c.showPage()
    c.save()
    if sys.platform.startswith('linux'):
        os.system('xdg-open "%s"' % default_output_file)
    else:
        os.system('start "%s"' % default_output_file)


if __name__=='__main__':
    main()
