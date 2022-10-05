#!/usr/bin/env python

import subprocess
import sys
import time

from pyperclip import paste

MARKER = "{}"

args = sys.argv[1:]
if not any(MARKER in arg for arg in args):
    args.append(MARKER)

old = paste()

while True:
    time.sleep(0.1)
    new = paste()
    if new != old:
        subprocess.call([arg.replace(MARKER, new) for arg in args])
        old = new
