#!/usr/bin/env python

from __future__ import print_function

import socket
import argparse
import platform

parser = argparse.ArgumentParser()
parser.add_argument('addr', help='IP to bind to', default='0.0.0.0', nargs='?')
parser.add_argument('port', help='UDP port to bind to', type=int, default=5005, nargs='?')
parser.add_argument('--reuse', '-r', action='store_true', help='Set SO_REUSEADDR on socket')
parser.add_argument('--echo', '-e', action='store_true', help='Echo the message back after receiving')
args = parser.parse_args()

UDP_IP = args.addr
UDP_PORT = args.port

sock = None
try:
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    if args.reuse:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((UDP_IP, UDP_PORT))

    print('Listening on {}:{}'.format(UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        print("received message: >%s<" % data)
        print("  received from:", addr)
        if args.echo:
            prefix = platform.uname()[1].encode() + b' echoing: '
            print('Sending back:', prefix+data)
            sock.sendto(prefix+data, addr)
        if data == b'bye':
            print('Exit command issued.')
            break
finally:
    sock.close()
