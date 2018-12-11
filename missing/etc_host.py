#!/usr/bin/env python
# this script now has a bigger brother: network/dig.py
# which can even append to /etc/hosts

from __future__ import print_function

import socket
import sys

print(socket.gethostbyname(sys.argv[1]), sys.argv[1])
