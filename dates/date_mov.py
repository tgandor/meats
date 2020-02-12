#!/usr/bin/env python

from __future__ import print_function

# usage: date_mov.py dscn0001.mov

import datetime
import glob
import os
import re
import struct
import sys
import time

# this is getting big. Maybe another approach is faster:
# https://stackoverflow.com/questions/21355316/getting-metadata-for-mov-video
# (would need to measure how many the while True loop reads...

chunk = 2**20

# mov_epoch = datetime.datetime(1903, 12, 31, 23, 24)
mov_epoch = datetime.datetime(1904, 1, 1, 0, 0)


def info(f):
    with open(f, 'rb') as file_:
        file_.seek(-chunk, os.SEEK_END)
        sample = file_.read()
        # idx = sample.find(b'mvhd')
        # print('idx:', idx, 'total:', len(sample) - idx, '/', len(sample))
    try:
        td = datetime.timedelta(seconds=struct.unpack('>I', re.search(b'mvhd.{4}(.{4})', sample).group(1))[0])
        dt = mov_epoch + td
        # This doesn't work on Windows - negative timestamps crash
        # dt = datetime.datetime.fromtimestamp(
        #     float(struct.unpack('>I', re.search(b'mvhd.{4}(.{4})', sample).group(1))[0])
        #     + time.mktime(datetime.datetime(1903, 12, 31, 23, 24).timetuple())
        # )
    except AttributeError as e:
        print(e, file=sys.stderr)
        print('{} - not found'.format(f))
    else:
        print('{} ; {}'.format(f, time.strftime("%Y-%m-%d (%a) %H:%M:%S", dt.timetuple())))


if __name__ == '__main__':
    for pattern in sys.argv[1:]:
        for fn in glob.glob(pattern):
            info(fn)
