#!/usr/bin/env python

# This looks for the image date embedded in jpeg header
#

# usage: date_jpg.py dscn0001.jpg...

from __future__ import print_function

import glob
import os
import re
import sys
import time


def grep_date(filename):
    some_data = open(filename, 'rb').read(2 ** 12)
    match = re.search(b'\d{4}([ :]\d\d){5}', some_data)
    if match:
        return match.group().decode()
    return None


def info(f):
    if not os.path.exists(f) and '*' in f:
        for i in glob.glob(f):
            info(i)
        return

    match = grep_date(f)
    if not match:
        print('{} - not found'.format(f))
        return
    try:
        parsed = time.strptime(match, "%Y:%m:%d %H:%M:%S")
        print('{} ; {}'.format(f, time.strftime("%Y-%m-%d (%a) %H:%M:%S", parsed)))
    except ValueError:
        print('{} ; error parsing: {}'.format(f, match), file=sys.stderr)


if __name__ == '__main__':
    for filename in sys.argv[1:]:
        info(filename)
