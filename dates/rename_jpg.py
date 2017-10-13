#!/usr/bin/env python

# usage: rename_jpg.py dscn0001.jpg...
# see also: exif_rename.sh (where possible)

import os
import re
import sys
import time
from glob import glob

strftime_format = '%Y%m%d_%H%M%S.jpg'


def classify(iterable, func):
    results = {False: [], True: []}
    for i in iterable:
        results[func(i)].append(i)
    return results.values()


def rename(f):
    if not os.path.exists(f) and '*' in f:
        for i in glob(f):
            rename(i)
        return

    some_data = open(f, 'rb').read(2 ** 12)
    date_match = re.search(b'\d{4}([ :]\d\d){5}', some_data)

    if not date_match:
        print('No date information in: {}'.format(f))
        return

    parsed = time.strptime(date_match.group().decode(), "%Y:%m:%d %H:%M:%S")
    new_name = time.strftime(strftime_format, parsed)

    if not os.path.exists(new_name):
        print('{} -> {}'.format(f, new_name))
        os.rename(f, new_name)
    else:
        print('{} -!> {} (file exists)'.format(f, new_name))


if __name__ == '__main__':
    args, opts = classify(sys.argv[1:], lambda x: x.startswith('-'))
    # print (opts, args)
    list(map(rename, args))
