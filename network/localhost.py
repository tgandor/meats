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

if sys.platform == 'win32':
    # 8-bit encodings...
    # config = os.popen('ipconfig').read()
    import subprocess
    config, _ = subprocess.Popen('ipconfig', stdout=subprocess.PIPE).communicate()
    regexp = r'IP(?:v4)? Address(?:[ .]*):\s*([0-9.]+)'.encode()
else:
    config = os.popen('ifconfig').read()
    regexp = 'inet (?:addr:)?([0-9.]+)'

for ip in re.findall(regexp, config):
    if type(ip) is bytes:
        ip = ip.decode()

    if ip == '127.0.0.1':
        continue

    print("http://%s%s%s" % (ip, port, path))
