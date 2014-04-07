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

regexp = "inet addr:([0-9.]+)"
config = os.popen('ifconfig').read()

if not config:
    # Windows
    config = os.popen('ipconfig').read()
    regexp = "IPv4 Address. . . . . . . . . . . : ([0-9.]+)"

for ip in re.findall(regexp, config):
    if ip == '127.0.0.1':
        continue
    print "http://%s%s%s" % (ip, port, path)
