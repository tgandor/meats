#!/usr/bin/env python

# usage: rename_avi.py dscn0001.jpg...

import os
import re
import sys
import time

strftime_format = '%y%m%d_%H%M%S.avi'


def rename(f):
    some_data = open(f, 'rb').read(2**11)
    date_string = re.search(b'([A-Z][a-z]{2} ){2}\d\d?([ :]\d\d){4}\d\d', some_data).group().decode()
    # print(date_string)
    parsed_date = time.strptime(date_string, "%a %b %d %H:%M:%S %Y")
    target_filename = time.strftime(strftime_format, parsed_date)
    if not os.path.exists(target_filename):
        print('{} -> {}'.format(f, target_filename))
        os.rename(f, target_filename)
    else:
        print('{} -!> {} : target exists'.format(f, target_filename))


if __name__=='__main__':
    list(map(rename, sys.argv[1:]))
