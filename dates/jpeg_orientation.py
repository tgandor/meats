#!/usr/bin/env python

"""
Actually, there is already a native program for that - jpegexiforient
Anyway, this does it en masse, recursively through CWD.
"""

from __future__ import print_function
import os
import sys

try:
    import piexif
except ImportError:
    print('Missing piexif')
    os.system('pip install piexif')
    exit()

for directory, _, files in os.walk('.'):
    for basename in files:
        filename = os.path.join(directory, basename)
        if basename.lower().endswith('.jpg') or basename.lower().endswith('.jpeg'):
            try:
                exif = piexif.load(filename)
            except:
                xi = sys.exc_info()
                print(filename, '-', xi[0].__name__, 'while loading:', xi[1], file=sys.stderr)
                continue

            print(filename, exif["0th"].get(piexif.ImageIFD.Orientation, 'None'), sep='\t')
