#!/usr/bin/env python

from __future__ import print_function

import argparse
import datetime
import re
import time

try:
    import Tkinter as Tk
    tk = Tk
except ImportError:
    # welcome to Python3
    import tkinter as tk
#def


def replace_dmy_with_iso(dmy_match):
    day, month, year = [int(x) for x in dmy_match.group().split('.')]
    global args
    weekday = datetime.datetime(year, month, day).strftime(' (%a)') if args.weekday else ''
    return '{:4d}-{:02d}-{:02d}{}'.format(year, month, day, weekday)


parser = argparse.ArgumentParser()
parser.add_argument('--weekday', '-w', action='store_true')
parser.add_argument('--debug', '-v', action='store_true')
args = parser.parse_args()

r = tk.Tk()
r.withdraw()
r.deiconify()
old_clipboard = r.clipboard_get()
print('Starting with clipboard:', old_clipboard)


def update_clipboard():
    global r
    global old_clipboard

    clipboard = r.clipboard_get()

    if args.debug:
        print('Clipboard now:', clipboard)

    if clipboard == old_clipboard:
        r.after(1000, update_clipboard)
        return

    replaced = re.sub(r'\d{1,2}\.\d{1,2}\.\d{4}', replace_dmy_with_iso, clipboard)
    print('Replacing "{}" with "{}"'.format(clipboard, replaced))

    r.clipboard_clear()
    r.clipboard_append(replaced)
    time.sleep(2.0)

    old_clipboard = replaced
    r.after(500, update_clipboard)


update_clipboard()
r.mainloop()
