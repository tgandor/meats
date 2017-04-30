#!/usr/bin/env python

from __future__ import print_function

# Description outdated:
# This is a oneliner to print the creation date in a mov file
# developed with python -c ;)

# usage: date_mov.py dscn0001.mov

import datetime
import os
import re
import struct
import sys
import time

chunk = 2**14


def info(f):
    with open(f) as file_:
        file_.seek(-chunk, os.SEEK_END)
        sample = file_.read()
    dt = datetime.datetime.fromtimestamp(
        float(struct.unpack('>I', re.search(b'mvhd.{4}(.{4})', sample).group(1))[0])
        + time.mktime(datetime.datetime(1903, 12, 31, 23, 24).timetuple())
    )
    print('{} ; {}'.format(f, time.strftime("%Y-%m-%d (%a) %H:%M:%S", dt.timetuple())))

if __name__=='__main__':
    list(map(info, sys.argv[1:]))
