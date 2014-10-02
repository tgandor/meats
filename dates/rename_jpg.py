#!/usr/bin/env python

# This looks for the image date embedded in jpeg header
#

# usage: rename_jpg.py dscn0001.jpg

import os
import re
import sys

def rename(f):
    some_data = open(f).read(2**11)
    new_name = re.search('\d{4}([ :]\d\d){5}', some_data).group().replace(' ', '_').replace(':', '-') + '.jpg'
    if not os.path.exists(new_name):
        print f, '->', new_name
        os.rename(f, new_name)
    else:
        print f, '-!>', new_name, '(file exists)'

if __name__=='__main__':
    map(rename, sys.argv[1:])
