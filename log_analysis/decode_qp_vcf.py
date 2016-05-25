#!/usr/bin/env python

import quopri
import sys

encoding = ';CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE'

while True:
    line = sys.stdin.readline()
    if not line:
        break
    if encoding in line:
        # seemingly this marks line continuation
        while line.strip().endswith('='):
            line = line.strip()[:-1] + sys.stdin.readline()
        line = quopri.decodestring(line.replace(encoding, ''))
    sys.stdout.write(line)
