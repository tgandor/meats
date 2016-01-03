#!/usr/bin/env python

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

font_size = 16
width = 11*cm
height = 16*cm
fonts_to_try = ['Ubuntu-L', 'Verdana', 'Arial']


def _setup_canvas(outfile='hello.pdf'):
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


def label(c, text, width=width, height=height):
    c.saveState()
    c.setDash(2, 8)
    inv = lambda x: A4[1]-x
    c.line(0, inv(height), width, inv(height))
    c.line(width, inv(0), width, inv(height))
    c.drawCentredString(width/2, inv((height+font_size)/2), text)
    c.setFontSize(12)
    c.drawCentredString(width/2, inv(height)+.5*cm, datetime.datetime.now().strftime('%Y-%m-%d (%a) %H:%M'))
    c.restoreState()


custom = raw_input('Enter label text: ') or 'Default label...'
c = _setup_canvas()
label(c, custom)
c.showPage()
c.save()
