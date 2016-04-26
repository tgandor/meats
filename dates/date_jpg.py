#!/usr/bin/env python

# This looks for the image date embedded in jpeg header
#

# usage: date_jpg.py dscn0001.jpg...

import re
import sys
import datetime
import time


def grep_date(filename):
    some_data = open(filename).read(2**14)
    match = re.search('\d{4}([ :]\d\d){5}', some_data)
    if match:
        return match.group()
    return None


def file_date(filename):
    date_time_str = grep_date(filename)
    if not date_time_str:
        return None
    date_str = date_time_str.split()[0]
    y, m, d = map(int, date_str.split(':'))
    return datetime.date(y, m, d)


def info(f):
    match = grep_date(f)
    if not match:
        print('{} - not found'.format(f))
        return
    parsed = time.strptime(match, "%Y:%m:%d %H:%M:%S")
    print('{} ; {}'.format(f, time.strftime("%Y-%m-%d (%a) %H:%M:%S", parsed)))


if __name__=='__main__':
    map(info, sys.argv[1:])
