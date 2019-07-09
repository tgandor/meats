#!/usr/bin/env python

"""
Actually, there is already a native program for that - jpegexiforient
Anyway, this does it en masse, recursively through CWD.

For the orientation meanings see:
http://sylvana.net/jpegcrop/exif_orientation.html

Value   0th Row     0th Column      Description of STORED image
---------------------------------------------------------------------
1	    top	        left side       unchanged
2	    top	        right side      flipped horizontally (selfie?)
3	    bottom	    right side      rotated 180 (upside down)
4	    bottom  	left side       flipped vertically
5	    left side	top             transposed (mirrored by 45' axis)
6	    right side	top             rotated -90' (left)
7	    right side	bottom          mirrored by -45' axis (rare)
8	    left side	bottom          rotated 90' (right)

Except 6 and 8, all the transforms are self-inverse (involutions).
f(f(x)) = x, in other words. This means they are applied again to obtain
the correct image.

In case of f_6 and f_8, they are eachother's opposites, i.e.:
f_6(f_8(x)) = x = f_8(f_6(x))

For orientation 6:

- the data in the file is rotated 90' left
- the viewer will rotate it 90' right to display
- the camera was rotated right (left hand above)
- (my) phone is taking vertical picture on main camera
- (my) phone is taking a selfie upside down

Note, the viewer needs to rotate the image in the same direction that
the camera was rotated. Also, the physical image on the sensor was flipped
against both axes, which gives a 180 rotation (like orientation 3).
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
    for basename in sorted(files):
        filename = os.path.join(directory, basename)
        if basename.lower().endswith('.jpg') or basename.lower().endswith('.jpeg'):
            try:
                exif = piexif.load(filename)
            except:
                xi = sys.exc_info()
                print(filename, '-', xi[0].__name__, 'while loading:', xi[1], file=sys.stderr)
                continue

            print(filename, exif["0th"].get(piexif.ImageIFD.Orientation, 'None'), sep='\t')
