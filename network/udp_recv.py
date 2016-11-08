#!/usr/bin/env python

import sys
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5005 # dummy

args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
opts = set(arg for arg in sys.argv[1:] if arg.startswith('-'))

if len(args) == 2:
    UDP_IP, UDP_PORT = args
elif len(args) == 1:
    UDP_PORT = int(args[0])
else:
    print("""Usage: {} [-r] [ADDRESS] PORTj

  -r - add SO_REUSEADDR option for binding.  """.format(sys.argv[0]))
    exit()

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

if '-r' in opts:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((UDP_IP, UDP_PORT))

print('Listening on {}:{}'.format(UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print "received message: >%s<" % data
    print "  received from:", addr
    if data == 'bye':
        break
