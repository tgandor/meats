#!/usr/bin/env python

# This looks for the image date embedded in jpeg header
#

# usage: date_jpg.py dscn0001.jpg...

import re
import sys

def info(f):
    some_data = open(f).read(2**11)
    print f, re.search('\d{4}([ :]\d\d){5}', some_data).group()

if __name__=='__main__':
    map(info, sys.argv[1:])


