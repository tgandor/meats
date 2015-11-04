import sys

try:
    from Tkinter import Tk
except ImportError:
    # welcome to Python3
    from tkinter import Tk
    raw_input = input

r = Tk()
r.withdraw()
r.clipboard_clear()
if len(sys.argv) < 2:
    r.clipboard_append(sys.stdin.read())
else:
    r.clipboard_append(' '.join(sys.argv[1:]))
r.destroy()

if sys.platform != 'win32':
    raw_input('Data was copied into clipboard. Paste and press ENTER to exit...')
