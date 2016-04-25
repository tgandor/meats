#!/usr/bin/env python
# This looks for the video date embedded in avi _junk_
# It only works with specific avi from some Olympus camera

# usage: date_avi.py pmdd0001.avi

import re
import sys
import time

if __name__=='__main__':
    some_data = open(sys.argv[1]).read(2**11)
    date_string = re.search('([A-Z][a-z]{2} ){2}\d\d?([ :]\d\d){4}\d\d', some_data).group()
    print(date_string)
    parsed_date = time.strptime(date_string, "%a %b %d %H:%M:%S %Y")
    print(time.strftime("%Y-%m-%d %H:%M:%S", parsed_date))
