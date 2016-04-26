#!/usr/bin/env python
# This looks for the video date embedded in avi _junk_
# It only works with specific avi from some Olympus camera

# usage: date_avi.py pmdd0001.avi

import re
import sys
import time

def info(f):
    some_data = open(f).read(2**11)
    date_string = re.search('([A-Z][a-z]{2} ){2}\d\d?([ :]\d\d){4}\d\d', some_data).group()
    # print(date_string)
    parsed_date = time.strptime(date_string, "%a %b %d %H:%M:%S %Y")
    print('{} ; {}'.format(f, time.strftime("%Y-%m-%d (%a) %H:%M:%S", parsed_date)))

if __name__=='__main__':
    map(info, sys.argv[1:])
