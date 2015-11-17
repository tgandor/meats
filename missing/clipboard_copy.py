#!/usr/bin/env python

import sys

try:
    import Tkinter as Tk
except ImportError:
    # welcome to Python3
    import tkinter as Tk
    raw_input = input

r = Tk.Tk()
r.withdraw()
r.clipboard_clear()

if len(sys.argv) < 2:
    data = sys.stdin.read()
else:
    data = ' '.join(sys.argv[1:])

r.clipboard_append(data)

if sys.platform != 'win32':
    if len(sys.argv) > 1:
        raw_input('Data was copied into clipboard. Paste and press ENTER to exit...')
    else:
        # stdin already read; use GUI to exit
        print('Data was copied into clipboard. Paste, then close popup to exit...')
        Tk.Button(r, text='Click or press key to exit', command=r.destroy, width=40, height=10).pack(fill=Tk.BOTH)
        r.title('Clipboard Copy')
        r.bind('<Key>', lambda e: r.destroy())
        r.deiconify()
        r.mainloop()
else:
    r.destroy()

