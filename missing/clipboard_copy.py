#!/usr/bin/env python

import argparse
import queue
import sys
import threading


def copy(data, wait_gui=False):
    try:
        import Tkinter as Tk

        tk = Tk
    except ImportError:
        # welcome to Python3
        import tkinter as tk

    pill_q = queue.Queue()

    r = tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(data)

    def read_stdin(q):
        sys.stdin.read(1)  # not all, just whatever
        q.put(True)  # sending death pill

    def poll():
        if pill_q.empty():
            r.after(100, poll)
        else:
            r.destroy()

    if not wait_gui:
        print("Data was copied into clipboard. Paste and press ENTER to exit...")
        # This won't work: RuntimeError: Calling Tcl from different apartment
        """
        gui_thread = threading.Thread(target=r.mainloop)
        gui_thread.setDaemon(True)
        gui_thread.start()
        """
        # such an overkill, but this is how it can work:
        # https://effbot.org/zone/tkinter-threads.htm
        threading.Thread(target=read_stdin, args=(pill_q,)).start()
        r.after(100, poll)
        r.mainloop()
    else:
        # stdin already read; use GUI to exit
        print("Data was copied into clipboard. Paste, then close popup to exit...")
        tk.Button(
            r, text="Click or press key to exit", command=r.destroy, width=40, height=10
        ).pack(fill=tk.BOTH)
        r.title("Clipboard Copy")
        r.bind("<Key>", lambda e: r.destroy() if e.keysym != "Alt_L" else None)
        r.deiconify()
        r.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--strip", "-s", action="store_true")
    parser.add_argument(
        "--gui", "-g", action="store_true", help="Use GUI (always when reading stdin)."
    )
    parser.add_argument("args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    data = " ".join(args.args) if args.args else sys.stdin.read()
    if args.strip:
        data = data.strip()
    if not args.args:
        copy(data, True)
    else:
        copy(data, args.gui)
