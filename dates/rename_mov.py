#!/usr/bin/env python

from __future__ import print_function

# usage: rename_mov.py dscn0001.mov...
# see also: exif_rename.sh (where possible)
# note: this script also works for .mp4 files (with right metadata...)

import datetime
import glob
import os
import re
import struct
import sys
import time

dry_run = False
strftime_format = '%Y%m%d_%H%M%S'
sample_len = 2**20
mov_epoch = datetime.datetime(1904, 1, 1, 0, 0)


def classify(iterable, func):
    results = {False: [], True: []}
    for i in iterable:
        results[func(i)].append(i)
    return results.values()


def rename(f):
    ext =  os.path.splitext(f)[1].lower()
    if ext not in ('.mov', '.mp4') :
        print('Not a mov file:', f)
        return

    with open(f, 'rb') as stream:
        stream.seek(-sample_len, os.SEEK_END)
        some_data = stream.read(sample_len)
    date_match = re.search(b'mvhd.{4}(.{4})', some_data)

    if not date_match:
        print('No date information (mvhd) in: {}'.format(f))
        return

    # import code; code.interact(local=locals())
    # print(len(some_data), date_match.span())
    # return

    time_delta = datetime.timedelta(seconds=struct.unpack('>I', date_match.group(1))[0])
    parsed = (mov_epoch + time_delta).timetuple()

    # Problem on Windows; funnily timedelta needs no 36 min hack...
    # parsed = datetime.datetime.fromtimestamp(
    #     float(struct.unpack(">I", date_match.group(1))[0])
    #     + time.mktime(datetime.datetime(1903, 12, 31, 23, 24).timetuple())
    # ).timetuple()

    new_name = os.path.join(
        os.path.dirname(f),
        time.strftime(strftime_format, parsed) + ext
    )

    if not os.path.exists(new_name):
        print('{} -> {}'.format(f, new_name))
        if not dry_run:
            os.rename(f, new_name)
    else:
        print('{} -!> {} (file exists)'.format(f, new_name))


if __name__=='__main__':
    args, flags = classify(sys.argv[1:], lambda x: x.startswith('-'))

    if '-n' in flags:
        print('(simulation)')
        dry_run = True

    for p in args:
        for mov in glob.glob(p):
            rename(mov)
