#!/usr/bin/env python

import sys
import re

lines = map(lambda x: x.strip().decode('utf-8'), open(sys.argv[1]))
dialog = re.compile('- [A-Z]')

paragraphs = [[]]

for line in lines:
    if len(line) == 0:
        paragraphs.append([])
        continue
    while True:
        m = dialog.search(line)
        if not m:
            break
        paragraphs[-1].append(line[:m.start()])
        paragraphs.append(['- '])
        line = line[m.end()-1:]
    paragraphs[-1].append(line)

print """<html>
  <head>
    <title>%s</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  </head>
  <body>""" % sys.argv[1]
for p in paragraphs:
    print '    <p>'+u" ".join(p).encode('utf-8')+'</p>'
print "</body></html>"

