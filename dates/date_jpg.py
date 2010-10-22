#!/usr/bin/env python

# This looks for the image date embedded in jpeg header
# 

# usage: date_mov.py dscn0001.jpg

import re
import sys

if __name__=='__main__':
    some_data = open(sys.argv[1]).read(2**11)
    print re.search('\d{4}([ :]\d\d){5}', some_data).group()

