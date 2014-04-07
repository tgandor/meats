#!/usr/bin/env python

import os
import re
import sys

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = '/'

if len(sys.argv) > 2:
    port = sys.argv[2]
    if not port.startswith(':'):
        port = ':' + port
else:
    port = ''

if not path.startswith('/'):
    path = '/' + path

config = os.popen('ifconfig').read()

for ip in re.findall("inet addr:([0-9.]+)", config):
    if ip == '127.0.0.1':
        continue
    print "http://%s%s%s" % (ip, port, path)
