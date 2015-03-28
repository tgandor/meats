#!/usr/bin/env python

import socket
import sys

print socket.gethostbyname(sys.argv[1]), sys.argv[1]

