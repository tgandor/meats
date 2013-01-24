#!/usr/bin/env python

import sys
import re

lines = map(lambda x: x.strip().decode('utf-8'), open(sys.argv[1]))

paragraphs = [[]]

carry = False
longl = True
roman = re.compile("[IVX]+$")

for line in lines:
    if len(line) == 0:
        continue # skip empty lines

    if roman.match(line):
        paragraphs.append([line])
        paragraphs.append([])
        longl = True
        carry = False
        continue # special treatment of section (roman) numbers

    if line.endswith(unichr(733)):
        newcarry = True
        line = line[:-1]
    else:
        newcarry = False

    if line.startswith(unichr(12)):
        line = line[:1]
        carry = True

    if carry:
        if len(paragraphs[-1]) > 0:
            paragraphs[-1][-1] += line
        else:
            paragraphs[-1].append(line)
        if len(line) < 100:
            longl = not longl
    else:
        if len(line) > 80:
            paragraphs[-1].append(line)
        elif longl:
            paragraphs[-1].append(line)
            if len(line) > 60:
                longl = False
            else:
                paragraphs.append([])
        else: # shortl
            if len(line) < 50:
                paragraphs[-1].append(line)
                longl = True
            else:
                paragraphs.append([line])

    carry = newcarry

print """<html>
  <head>
    <title>%s</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  </head>
  <body>""" % sys.argv[1]
for p in paragraphs:
    print '    <p>', u" ".join(p).encode('utf-8'), '</p>'
print "</body></html>"

