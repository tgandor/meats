#!/usr/bin/env python

# This, of corrs, works under X11, like under Linux etc.
# source:
# http://askubuntu.com/questions/80254/how-do-i-turn-off-caps-lock-the-lock-not-the-key-by-command-line

from ctypes import *
X11 = cdll.LoadLibrary("libX11.so.6")
display = X11.XOpenDisplay(None)
X11.XkbLockModifiers(display, c_uint(0x0100), c_uint(2), c_uint(0))
X11.XCloseDisplay(display)
