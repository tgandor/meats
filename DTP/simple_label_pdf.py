#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

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
    from reportlab.pdfbase.ttfonts import TTFont, TTFError
except ImportError:
    print('Missing reportlab, trying to install...')
    os.system("sudo apt-get install python{}-reportlab".format(
        '3' if sys.version_info.major == 3 else ''))
    exit()

parser = argparse.ArgumentParser()
parser.add_argument('--font-size', type=int, default=20)
parser.add_argument('--repeat', type=int, default=1, help="Times to repeat each label verbatim (without series)")
parser.add_argument('--print', action='store_true', help="Try to print directly, instead of opening")
parser.add_argument('--gui', action='store_true', help="Open a tkinter GUI to create labels")
parser.add_argument('args', type=str, nargs='*', help='Old arguments.')

settings = dict(
    font_size=20
)
date_font = 12
default_text = 'Example label'
default_width = 21 * cm
default_height = 28.5 * cm
top_margin = 0.0 * cm
bottom_margin = 1.0 * cm
line_width = 0.25
default_length = None
default_output_file = os.path.join(tempfile.gettempdir(), 'simple_label_output.pdf')

fonts_to_try = ['Ubuntu-L', 'Verdana', 'Arial', 'DejaVuSans']

last_font = []  # needs to be reloaded after new page


def _setup_canvas(outfile=default_output_file):
    for font_name in fonts_to_try:
        try:
            font = TTFont(font_name, font_name + '.ttf')
            pdfmetrics.registerFont(font)
            font_to_use = font_name
            break
        except TTFError:
            font_to_use = None

    c = canvas.Canvas(outfile)
    if font_to_use:
        c.setFont(font_to_use, settings['font_size'])
        last_font.append(font_to_use)
    else:
        sys.stderr.write('No TTF font found from list: {}\n'.format(', '.join(fonts_to_try)))
    c.setTitle(outfile)
    return c


def new_page(c):
    c.showPage()
    if last_font:
        c.setFont(last_font[0], settings['font_size'])


class LabelState:
    horizontal = False
    height_left = A4[1] - top_margin


def label(c, text, width=default_width, height=default_height, state=LabelState()):
    # convenience hack
    width, height = [min(x, max(A4)) for x in (width, height)]

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
    inv = lambda x: page_height - x

    c.saveState()
    c.setDash(4, 8)
    c.setLineWidth(line_width)

    # seems like transform IS part of state
    if line_width > 0 and state.height_left < page_height:  # - top_margin:
        c.line(0, state.height_left, page_width, state.height_left)
    h_offset = state.height_left - page_height
    c.translate(0, h_offset)

    # borders
    if line_width > 0:
        c.line(0, inv(height), width, inv(height))
        c.line(width, inv(0), width, inv(height))

    # text breaking...
    font_size = settings['font_size']
    lines = text.split('\n')
    extra_h = len(lines) / 2 * font_size * (-1)
    for line, i in zip(lines, range(len(lines))):
        # serial label: last line should be with date font
        if i == len(lines) - 1 and re.match(r'\d+/\d+$', line):
            c.setFontSize(date_font)
        c.drawCentredString(width / 2, inv((height + font_size) / 2 + extra_h), line)
        extra_h += font_size

    # date subscript
    c.setFontSize(date_font)
    c.drawCentredString(width / 2, max(inv(height) + .5 * cm, bottom_margin),
                        datetime.datetime.now().strftime('%Y-%m-%d (%a) %H:%M'))

    # final cleanup
    c.restoreState()
    state.height_left -= height
    return True


# label persistence


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
    conn.text_factory = str  # which == unicode on Py3, and works!
    return conn, cursor


def close_database(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()


def save_label(text, width, height, length):
    conn, cursor = open_database()
    cursor.execute(u"SELECT id FROM labels WHERE text = ?", (text,))
    # create or update label
    label_id = cursor.fetchone()
    if length is not None:
        length /= cm
    if label_id is None:
        print('Creating label')
        cursor.execute("INSERT INTO labels (text, width, height, length) VALUES (?,?,?,?)",
                       (text, width / cm, height / cm, length,))
        label_id = cursor.lastrowid
    else:
        label_id = label_id[0]
        print('Updating label {}'.format(label_id))
        cursor.execute("UPDATE labels SET width=?, height=?, length=? WHERE id=?",
                       (width / cm, height / cm, length, label_id))
    # log the generation
    cursor.execute("INSERT INTO outprints(label_id, outprint_date) VALUES (?,?)",
                   (label_id, datetime.datetime.now()))
    close_database(conn, cursor)


def _finish_rendering(canvas):
    canvas.showPage()
    canvas.save()
    print_ = getattr(args, 'print')
    if sys.platform.startswith('linux'):
        if print_:
            os.system('lp "%s"' % default_output_file)
        else:
            os.system('xdg-open "%s"' % default_output_file)
    else:
        os.startfile(default_output_file, 'print' if print_ else 'open')


def multi_label(text, width, height, count):
    save_label(text, width, height, None)
    c = _setup_canvas()
    state = LabelState()
    for i in range(count):
        label(c, u'{}\n{}/{}'.format(text, i + 1, count), width, height, state=state)
    _finish_rendering(c)


def parse_s(s, full_s, max_s=A4[1]):
    if s.endswith('%'):
        return float(s[:-1]) / 100 * full_s
    val = float(s) * cm
    if val > max_s:
        print('Warning: value', val / cm, '>=', max_s / cm, '(clamped)')
        return max_s
    return val


def get_parameters():
    if len(argv) < 3:
        print('Not enough arguments. Usage: simple_label_pdf.py text W H [L]')
        exit()

    text = argv[0]
    in_width = argv[1]
    in_height = argv[2]
    width = parse_s(in_width, A4[0]) if in_width else default_width
    height = parse_s(in_height, A4[1]) if in_height else default_height

    if len(argv) >= 4:
        # A4[0], because length is like width
        length = parse_s(argv[3], A4[0])
    else:
        length = default_length

    return text, width, height, length


def main():
    text, width, height, length = get_parameters()
    save_label(text, width, height, length)
    c = _setup_canvas()
    for _ in range(args.repeat):
        label(c, text, width, height)
        if length:
            label(c, text, length, height)
            label(c, text, width, length)
    _finish_rendering(c)


def win_main():
    try:
        import Tkinter as tk
    except ImportError:
        import tkinter as tk

    ui_font = ('TkDefaultFont', 12)

    class Spinbox(tk.Spinbox):
        def __init__(self, *args, **kwargs):
            kwargs['font'] = ui_font
            kwargs['justify'] = 'right'
            tk.Spinbox.__init__(self, *args, **kwargs)
            self.bind('<MouseWheel>', self.mouse_wheel)
            self.bind('<Button-4>', self.mouse_wheel)
            self.bind('<Button-5>', self.mouse_wheel)

        def set(self, value):
            self.delete(0, tk.END)
            self.insert(0, value)
            return self

        def mouse_wheel(self, event):
            if event.num == 5 or event.delta == -120:
                self.invoke('buttondown')
            elif event.num == 4 or event.delta == 120:
                self.invoke('buttonup')

    def ui_label(parent, text):
        tk.Label(parent, text=text, font=ui_font).pack(anchor=tk.N)

    def generate(text_widget, width_input, height_input, is_serial, num_serial):
        label_text = text_widget.get('1.0', 'end').strip()
        w = float(width_input.get()) * cm
        h = float(height_input.get()) * cm
        if is_serial.get():
            multi_label(label_text, w, h, int(num_serial.get()))
        else:
            c = _setup_canvas()
            save_label(label_text, w, h, None)
            state = LabelState()
            for _ in range(int(num_serial.get())):
                label(c, label_text, w, h, state)
            _finish_rendering(c)

    root = tk.Tk()
    root.title('Simple Label')
    dialog = tk.Frame(root)

    ui_label(dialog, 'Label text:')
    text = tk.Text(dialog)
    text.focus_set()

    def modified(event):
        text.tag_add('label', '1.0', tk.END)

    text.tag_config('label', justify='center', font=(fonts_to_try[0], settings['font_size']))
    text.bind('<Key>', modified)
    text.bind('<<Modified>>', modified)
    text.pack(anchor=tk.N)

    ui_label(dialog, text='Width: [cm]')
    width = Spinbox(dialog, from_=0, to=30, increment=0.1, format="%.1f")
    width.set("21.0").pack(anchor=tk.N)

    ui_label(dialog, text='Height: [cm]')
    height = Spinbox(dialog, from_=0, to=30, increment=0.1, format="%.1f")
    height.set("8.0").pack(anchor=tk.N)

    ui_label(dialog, 'Repeat count:')
    serial_count = Spinbox(dialog, from_=1, to=100)
    serial_count.pack(anchor=tk.N)

    serial_flag = tk.IntVar()
    tk.Checkbutton(
        dialog, variable=serial_flag, font=ui_font,
        text='Generate serial labels').pack(anchor=tk.N)

    def change_font(font_variable):
        settings['font_size'] = int(font_variable.get())
        text.tag_config('label', font=(fonts_to_try[0], settings['font_size']))

    ui_label(dialog, 'Font size [pt]:')

    font_size = tk.IntVar(dialog, value=settings['font_size'])
    Spinbox(dialog, values=range(20, 74, 2), textvariable=font_size).pack(anchor=tk.N)
    font_size.trace('w', lambda *_: change_font(font_size))

    tk.Button(
        dialog, text='Generate', font=ui_font, width=50, height=3,
        command=lambda: generate(text, width, height, serial_flag, serial_count)
    ).pack(anchor=tk.N)
    dialog.pack(fill=tk.BOTH, expand=1)
    root.mainloop()


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    args = parser.parse_args(sys.argv[1:])
    argv = args.args
    settings['font_size'] = args.font_size
    if args.gui or len(argv) == 0:
        win_main()
    elif len(argv) == 4 and argv[3].startswith('x'):
        multi_label(argv[0], parse_s(argv[1], A4[0]), parse_s(argv[2], A4[1]), int(argv[3][1:]))
    else:
        main()
