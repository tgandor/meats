#!/usr/bin/env python
# This looks for the video date embedded in avi _junk_
# It only works with specific avi from some Olympus camera
# no guarantees ;)

# usage: date_avi.py pmdd0001.avi

import re
import sys

if __name__=='__main__':
    some_data = open(sys.argv[1]).read(2**11)
    print re.search('([A-Z][a-z]{2} ){2}\d\d?([ :]\d\d){4}\d\d', some_data).group()
