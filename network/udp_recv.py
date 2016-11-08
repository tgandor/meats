#!/usr/bin/env python

import sys
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

if len(sys.argv) == 3:
    UDP_IP, UDP_PORT = sys.argv[1:]
elif len(sys.argv) == 2:
    UDP_PORT = sys.argv[1]


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))

print('Listening on {}:{}'.format(UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print "received message: >%s<" % data
    print "  received from:", addr
    if data == 'bye':
        break
