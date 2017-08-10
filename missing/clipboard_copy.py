#!/usr/bin/env python

from __future__ import print_function

import sys


def copy(data, wait_gui=False):
    try:
        import Tkinter as Tk
        tk = Tk
    except ImportError:
        # welcome to Python3
        import tkinter as tk

    r = tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(data)

    if not wait_gui:
        print('Data was copied into clipboard. Paste and press ENTER to exit...')
        for _ in sys.stdin:
            break
        r.destroy()
    else:
        # stdin already read; use GUI to exit
        print('Data was copied into clipboard. Paste, then close popup to exit...')
        tk.Button(r, text='Click or press key to exit', command=r.destroy, width=40, height=10).pack(fill=tk.BOTH)
        r.title('Clipboard Copy')
        r.bind('<Key>', lambda e: r.destroy() if e.keysym != 'Alt_L' else None)
        r.deiconify()
        r.mainloop()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        copy(sys.stdin.read(), True)
    else:
        copy(' '.join(sys.argv[1:]))
