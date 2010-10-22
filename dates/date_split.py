#!/usr/bin/env python

# Move arguments to folders named after their 
# apparent date (creation / photo taken etc.)

# usage: date_split.py file1.jpg file2.mov ...

import re
import sys
import os

def date_mov(filename):
    """Return a (probable) date string found in a JPG file."""
    import time, datetime, struct
    fh = open(filename)
    # empyrical: 32kB should do
    fh.seek(-2**15, os.SEEK_END) 
    some_data = fh.read()
    m = re.search("mvhd.{4}(.{4})", some_data)
    # print "Found at: ", m.start(), 'of', len(some_data),'before',len(some_data)-m.start()
    return str(datetime.datetime.fromtimestamp(float(struct.unpack(">I", m.group(1))[0])+time.mktime(datetime.datetime(1904,1,1).timetuple())))[:10]

def date_jpg(filename):
    """Return a (probable) date string found in a JPG file."""
    # empyrical: 2kB should do
    some_data = open(filename).read(2**11)
    return re.search(
        '\d{4}([ :]\d\d){5}', some_data
        ).group()[:10].replace(':','-')

def date_avi(filename):
    """Return a (probable) date string found in some AVI files."""
    mon = dict(zip(
        'jan feb mar apr jun jul aug sep oct nov dec'.split(), range(1,13)
    ))
    some_data = open(sys.argv[1]).read(2**11)
    m = re.search(
        '([A-Z][a-z]{2}) ([A-Z][a-z]{2}) (\d\d?)([ :]\d\d){3} (\d{4})',
        some_data
    )
    return "%s-%02d-%02d" % (
        m.group(5), mon[m.group(2).lower()], int(m.group(3))
    ) # + ' ' + m.group()
    
def move_to_directory(filename):
    """Move file to directory named like the (probable) date string."""
    try:
        handlers = { 'jpg': date_jpg, 'mov': date_mov, 'avi': date_avi }
        the_date =  handlers[filename[-3:].lower()](filename)
        print filename, the_date
    except:
        print "Couldn't deal with:", filename

if __name__=='__main__':
    map(move_to_directory, sys.argv[1:])
