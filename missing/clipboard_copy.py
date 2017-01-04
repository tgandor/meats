#!/usr/bin/env python

import sys


def read(prompt):
    if sys.version_info.major == 2:
        return raw_input(prompt)
    return input(prompt)


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

    if sys.platform != 'win32':
        if not wait_gui:
            read('Data was copied into clipboard. Paste and press ENTER to exit...')
            r.destroy()
        else:
            # stdin already read; use GUI to exit
            print('Data was copied into clipboard. Paste, then close popup to exit...')
            tk.Button(r, text='Click or press key to exit', command=r.destroy, width=40, height=10).pack(fill=tk.BOTH)
            r.title('Clipboard Copy')
            r.bind('<Key>', lambda e: r.destroy() if e.keysym != 'Alt_L' else None)
            r.deiconify()
            r.mainloop()
    else:
        r.destroy()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        copy(sys.stdin.read(), True)
    else:
        copy(' '.join(sys.argv[1:]))
