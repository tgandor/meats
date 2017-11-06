#!/usr/bin/env python

from __future__ import print_function

import os
import pwd
import sys

# inspired by: https://scottlinux.com/2014/12/08/how-to-create-a-systemd-service-in-linux-centos-7/

template = """
[Unit]
Description={service} Service
After=network.target

[Service]
Type=simple
User={user}
ExecStart={executable}
Restart=on-abort


[Install]
WantedBy=multi-user.target
"""

if len(sys.argv) < 2:
    print('Usage: {0} executable [arguments...]'.format(sys.argv[0]))
    exit()

abspath = os.path.abspath(sys.argv[1])
basename = os.path.basename(abspath)

print(template.format(service=basename, user=pwd.getpwuid(os.getuid())[0], executable=' '.join([abspath] + sys.argv[2:])))

