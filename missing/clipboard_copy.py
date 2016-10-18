#!/usr/bin/env python

import sys


def copy(data, wait_gui=False):
    try:
        import Tkinter as Tk
    except ImportError:
        # welcome to Python3
        import tkinter as Tk
        raw_input = input

    r = Tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(data)

    if sys.platform != 'win32':
        if not wait_gui:
            raw_input('Data was copied into clipboard. Paste and press ENTER to exit...')
            r.destroy()
        else:
            # stdin already read; use GUI to exit
            print('Data was copied into clipboard. Paste, then close popup to exit...')
            Tk.Button(r, text='Click or press key to exit', command=r.destroy, width=40, height=10).pack(fill=Tk.BOTH)
            r.title('Clipboard Copy')
            r.bind('<Key>', lambda e: r.destroy() if e.keysym != 'Alt_L' else None)
            r.deiconify()
            r.mainloop()
    else:
        r.destroy()




if __name__ == '__main__':
    if len(sys.argv) < 2:
        data = sys.stdin.read()
        copy(data, True)
    else:
        data = ' '.join(sys.argv[1:])
        copy(data)
