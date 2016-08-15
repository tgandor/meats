#!/usr/bin/env python

# This looks for the image date embedded in jpeg header
#

# usage: date_jpg.py dscn0001.jpg...

import re
import sys
import datetime
import time


def grep_date(filename):
    some_data = open(filename, 'rb').read(2**12)
    match = re.search(b'\d{4}([ :]\d\d){5}', some_data)
    if match:
        return match.group().decode()
    return None


def info(f):
    match = grep_date(f)
    if not match:
        print('{} - not found'.format(f))
        return
    parsed = time.strptime(match, "%Y:%m:%d %H:%M:%S")
    print('{} ; {}'.format(f, time.strftime("%Y-%m-%d (%a) %H:%M:%S", parsed)))


if __name__=='__main__':
    list(map(info, sys.argv[1:]))
