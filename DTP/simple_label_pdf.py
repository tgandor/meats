#!/usr/bin/env python

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime
import os
import tempfile
import sys


font_size = 20
date_font = 12
default_text = 'Example label'
default_width = 20*cm
default_height = 10*cm
default_length = None
default_output_file = os.path.join(tempfile.gettempdir(), 'simple_label_output.pdf')
fonts_to_try = ['Ubuntu-L', 'Verdana', 'Arial']


last_font = []  # needs to be reloaded after new page


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
        last_font.append(font_to_use)
    c.setTitle(outfile)
    return c


def new_page(c):
    c.showPage()
    if last_font:
        c.setFont(last_font[0], font_size)


class LabelState:
    horizontal = False
    height_left = A4[1]


def label(c, text, width=default_width, height=default_height, state=LabelState()):
    # validate
    if min(width, height) > min(A4) or max(width, height) > max(A4):
        sys.stderr.write('Error: label too big: {0} - not generating.\n'.format((width, height)))
        return False

    # starting page width
    page_width, page_height = landscape(A4) if state.horizontal else A4

    # new page if can't fit
    if height > state.height_left:
        new_page(c)
        state.height_left = page_height

    # maybe switch to landscape
    if width > page_width:
        if state.height_left < page_height:
            new_page(c)
        c.setPageSize(landscape(A4))
        page_width, page_height = landscape(A4)
        state.horizontal = True
        state.height_left = page_height
        sys.stderr.write('Warning: switched to horizontal.\n')

    # maybe switch back to portrait
    if height > page_height:
        # page already shown
        c.setPageSize(A4)
        page_width, page_height = A4
        state.horizontal = False
        state.height_left = page_height
        sys.stderr.write('Warning: switched to vertical.\n')

    # coordinates inversion
    inv = lambda x: page_height-x

    c.saveState()
    c.setDash(4, 8)
    c.setLineWidth(0.25)

    # seems like transform not part of state...
    h_offset = 0
    if state.height_left < page_height:
        c.line(0, state.height_left, page_width, state.height_left)
        h_offset = state.height_left - page_height
        c.translate(0, h_offset)

    # borders
    c.line(0, inv(height), width, inv(height))
    c.line(width, inv(0), width, inv(height))

    # text breaking...
    lines = text.split('\n')
    extra_h = len(lines) / 2 * font_size * (-1)
    for line in lines:
        c.drawCentredString(width/2, inv((height+font_size)/2 + extra_h), line)
        extra_h += font_size

    # date subscript
    c.setFontSize(date_font)
    c.drawCentredString(width/2, inv(height)+.5*cm, datetime.datetime.now().strftime('%Y-%m-%d (%a) %H:%M'))

    # final cleanup
    c.restoreState()
    if h_offset != 0:
        c.translate(0, -h_offset)
    state.height_left -= height
    return True


def get_parameters():
    if len(sys.argv) < 2:
        text = raw_input('Enter label text: ') or default_text
    else:
        text = sys.argv[1]

    if len(sys.argv) < 3:
        in_width = raw_input('Width (%.1f): ' % (default_width/cm))
    else:
        in_width = sys.argv[2]
    width = float(in_width)*cm if in_width else default_width

    if len(sys.argv) < 4:
        in_height = raw_input('Height (%.1f): ' % (default_height/cm))
    else:
        in_height = sys.argv[3]
    height = float(in_height)*cm if in_height else default_height

    if len(sys.argv) >= 5:
        length = float(sys.argv[4]) * cm
    else:
        length = default_length

    return text, width, height, length


def main():
    text, width, height, length = get_parameters()
    c = _setup_canvas()
    label(c, text, width, height)
    if length:
        label(c, text, length, height)
        label(c, text, length, width)
    c.showPage()
    c.save()
    if sys.platform.startswith('linux'):
        os.system('xdg-open "%s"' % default_output_file)
    else:
        os.system('start "" "%s"' % default_output_file)


if __name__=='__main__':
    main()
