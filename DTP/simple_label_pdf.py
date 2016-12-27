#!/usr/bin/env python

import argparse
import datetime
import locale
import os
import re
import sqlite3
import sys
import tempfile


try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print('Missing reportlab, trying to install...')
    os.system("sudo apt-get install python{}-reportlab".format(
        '3' if sys.version_info.major == 3 else ''))
    exit()


font_size = 20
date_font = 12
default_text = 'Example label'
default_width = 21*cm
default_height = 28.5*cm
top_margin = 0.0*cm
bottom_margin = 1.0*cm
line_width = 0.25
default_length = None
default_output_file = os.path.join(tempfile.gettempdir(), 'simple_label_output.pdf')
fonts_to_try = ['Ubuntu-L', 'Verdana', 'Arial', 'DejaVuSans']



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
    else:
        sys.stderr.write('No TTF font found from list: {}\n'.format(', '.join(fonts_to_try)))
    c.setTitle(outfile)
    return c


def new_page(c):
    c.showPage()
    if last_font:
        c.setFont(last_font[0], font_size)


class LabelState:
    horizontal = False
    height_left = A4[1] - top_margin


def label(c, text, width=default_width, height=default_height, state=LabelState()):
    # validate
    if min(width, height) > min(A4) or max(width, height) > max(A4):
        sys.stderr.write('Error: label too big: {}x{} - not generating.\n'.format(width, height))
        return False

    # starting page width
    page_width, page_height = landscape(A4) if state.horizontal else A4

    # new page if can't fit
    if height > state.height_left:
        new_page(c)
        state.height_left = page_height - top_margin

    # maybe switch to landscape
    if width > page_width:
        if state.height_left < page_height:
            new_page(c)
        c.setPageSize(landscape(A4))
        page_width, page_height = landscape(A4)
        state.horizontal = True
        state.height_left = page_height - top_margin
        sys.stderr.write('Warning: switched to horizontal.\n')

    # maybe switch back to portrait
    if height > page_height:
        # page already shown
        c.setPageSize(A4)
        page_width, page_height = A4
        state.horizontal = False
        state.height_left = page_height - top_margin
        sys.stderr.write('Warning: switched to vertical.\n')

    # coordinates inversion
    inv = lambda x: page_height-x

    c.saveState()
    c.setDash(4, 8)
    c.setLineWidth(line_width)

    # seems like transform IS part of state
    if line_width > 0 and state.height_left < page_height: #  - top_margin:
        c.line(0, state.height_left, page_width, state.height_left)
    h_offset = state.height_left - page_height
    c.translate(0, h_offset)

    # borders
    if line_width > 0:
        c.line(0, inv(height), width, inv(height))
        c.line(width, inv(0), width, inv(height))

    # text breaking...
    lines = text.split('\n')
    extra_h = len(lines) / 2 * font_size * (-1)
    for line, i in zip(lines, range(len(lines))):
        # serial label: last line should be with date font
        if i == len(lines) - 1 and re.match(r'\d+/\d+$', line):
            c.setFontSize(date_font)
        c.drawCentredString(width/2, inv((height+font_size)/2 + extra_h), line)
        extra_h += font_size

    # date subscript
    c.setFontSize(date_font)
    c.drawCentredString(width/2, max(inv(height)+.5*cm, bottom_margin), datetime.datetime.now().strftime('%Y-%m-%d (%a) %H:%M'))

    # final cleanup
    c.restoreState()
    state.height_left -= height
    return True


def get_parameters():
    if sys.version_info.major == 3:
        raw_input = input
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


# label persistance

def open_database():
    labels_file = os.path.expanduser("~/labels.db")
    initialize = not os.path.exists(labels_file)
    conn = sqlite3.connect(labels_file)
    cursor = conn.cursor()
    if initialize:
        cursor.executescript("""
create table labels
(
    id integer not null primary key autoincrement,
    text contents not null,
    width decimal not null,
    height decimal not null,
    length decimal null
);

create table outprints
(
    id integer not null primary key autoincrement,
    label_id integer not null references labels(id),
    outprint_date datetime not null 
);
""")
    conn.text_factory = str # which == unicode on Py3, and works!
    return conn, cursor


def close_database(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()


def save_label(text, width, height, length):
    conn, cursor = open_database()
    cursor.execute(u"select id from labels where text = ?", (text,))
    # create or update label
    label_id = cursor.fetchone()
    if length is not None:
        length /= cm
    if label_id is None:
        print('Creating label')
        cursor.execute("insert into labels (text, width, height, length) values (?,?,?,?)",
                       (text, width / cm, height / cm, length, ))
        label_id = cursor.lastrowid
    else:
        label_id = label_id[0]
        print('Updating label {}'.format(label_id))
        cursor.execute("update labels set width=?, height=?, length=? where id=?",
                       (width / cm, height / cm, length, label_id))
    # log the generation
    cursor.execute("insert into outprints(label_id, outprint_date) values (?,?)",
                   (label_id, datetime.datetime.now()))
    close_database(conn, cursor)


def _finish_rendering(canvas):
    canvas.showPage()
    canvas.save()
    if sys.platform.startswith('linux'):
        os.system('xdg-open "%s"' % default_output_file)
    else:
        os.system('start "" "%s"' % default_output_file)


def multi_label(text, width, height, count):
    save_label(text, width, height, None)
    c = _setup_canvas()
    for i in range(count):
        label(c, '{}\n{}/{}'.format(text, i+1, count), width, height)
    _finish_rendering(c)


def main():
    text, width, height, length = get_parameters()
    save_label(text, width, height, length)
    c = _setup_canvas()
    label(c, text, width, height)
    if length:
        label(c, text, length, height)
        label(c, text, width, length)
    _finish_rendering(c)


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    if len(sys.argv) == 5 and sys.argv[4].startswith('x'):
        multi_label(sys.argv[1], float(sys.argv[2])*cm, float(sys.argv[3])*cm, int(sys.argv[4][1:]))
    else:
        main()
