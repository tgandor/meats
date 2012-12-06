#!/usr/bin/env python

import sys
import re

lines = sys.stdin.readlines()

first = {}
last = {}

rev = re.compile('r\d+')

for el in lines:
    if rev.match(el):
        fields = map(str.strip, el.split('|'))
	if fields[1] not in first:
	    first[fields[1]] = fields
        last[fields[1]] = fields

# detect backward log

hi, by = 'in', 'ou'
if len(first) > 0 and any( 
  int(first[key][0][1:]) > int(last[key][0][1:]) 
  for key in first.keys() ):
    hi, by = by, hi

results = sorted(
  [(int(val[0][1:]), val[2].split()[0], hi, val[1]) for val in first.values()]
  + 
  [(int(val[0][1:]), val[2].split()[0], by, val[1]) for val in last.values()]
)

for row in results:
    print "%6s %s %s %s" % row

