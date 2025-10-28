from __future__ import print_function

import os
import sys

if os.name != "nt":
    print("This program requres Microsoft Windows")  # remember DOS?
    exit()

# some inspiration:
# https://grokbase.com/t/python/python-list/014y2jyzwd/how-to-enumerate-all-drives-on-win32/oldest

try:
    import win32api

    drives_str = win32api.GetLogicalDriveStrings()
    drives = drives_str.split("\x00")[:-1]

    for drive in drives:
        print(drive)
except ImportError:
    print("Missing win32api", file=sys.stderr)
    import string

    for letter in string.ascii_uppercase:
        path = letter + ":\\"
        if os.path.exists(path):
            print(path)
