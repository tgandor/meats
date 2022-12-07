#!/usr/bin/env python

import argparse
import datetime
import re
import sys

TIME_FORMAT = "[%d/%b/%Y:%H:%M:%S %z]"
OUT_TIME_F = "%Y-%m-%d %H:%M:%S"


parser = argparse.ArgumentParser()
parser.add_argument("--logfile", "-l")
parser.add_argument("--regex", "-r", help="find in the log; use group to extract")
parser.add_argument("--sep", "-s", help="output separator", default=",")
parser.epilog = """
Example usage:
(cat /var/log/apache2/access.log{,.1}; zcat /var/log/apache2/access.log*gz) |
    ~/meats/log_analysis/apache_log_extract.py -r /robots.txt
"""
args = parser.parse_args()


log = open(args.logfile) if args.logfile else sys.stdin

for line in log:
    ls = line.split()
    tstr = " ".join(ls[3:5])
    ts = datetime.datetime.strptime(tstr, TIME_FORMAT)
    ostr = ts.strftime(OUT_TIME_F)
    if args.regex:
        data = re.search(args.regex, line)
        if not data:
            continue
        output = data.groups() or (data.group(),)
    else:
        output = ls[:1] + ls[5:]
    print(ostr, *output, sep=args.sep)
