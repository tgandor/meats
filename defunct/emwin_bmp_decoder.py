#!/usr/bin/env python

import os
import sys
import numpy as np
from PIL import Image

for arg in sys.argv[1:]:
    data = open(arg, 'rb').read()
    header = np.fromstring(data[:16], dtype=np.uint16)
    w, h = header[2], header[3]
    print('{}: {}x{}'.format(arg, w, h))
    if len(data) != 4 * w * h + 16:
        print('ERROR: total size: {}, calculated size: {}'.format(len(data), 4 * w * h + 16))
        continue

    # format unknown
    '''
    img_data = np.fromstring(data[16:w*h+16], dtype=np.uint8).reshape((h, w))
    # img_data = img_data[:, :, :3]
    img_data = img_data.reshape(())
    img = Image.fromarray(img_data)
    root, ext = os.path.splitext(arg)
    filename = root + '.png'
    img.save(filename)
    print('Saved {}.'.format(filename))
    '''