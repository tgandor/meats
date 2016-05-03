#!/usr/bin/env python

# Description outdated:
# This is a oneliner to print the creation date in a mov file
# developed with python -c ;)

# usage: date_mov.py dscn0001.mov

import time, datetime, struct, re, sys

def info(f):
    dt = datetime.datetime.fromtimestamp(
        float(struct.unpack(">I", re.search("mvhd.{4}(.{4})", open(f).read()).group(1))[0])
        + time.mktime(datetime.datetime(1904,1,1).timetuple())
    )
    print('{} ; {}'.format(f, time.strftime("%Y-%m-%d (%a) %H:%M:%S", dt.timetuple())))

if __name__=='__main__':
    map(info, sys.argv[1:])
