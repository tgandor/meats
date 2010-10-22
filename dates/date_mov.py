#/usr/bin/env python

# This is a oneliner to print the creation date in a mov file
# developed with python -c ;)

# usage: date_mov.py dscn0001.mov

if __name__=='__main__':
    import time, datetime, struct, re, sys; print datetime.datetime.fromtimestamp(float(struct.unpack(">I", re.search("mvhd.{4}(.{4})", open(sys.argv[1]).read()).group(1))[0])+time.mktime(datetime.datetime(1904,1,1).timetuple()))

