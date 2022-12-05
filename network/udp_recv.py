#!/usr/bin/env python

from __future__ import print_function

import argparse
import datetime
import platform
import socket

parser = argparse.ArgumentParser()
parser.add_argument("addr", help="IP to bind to", default="0.0.0.0", nargs="?")
parser.add_argument("--port", "-p", help="UDP port to bind to", type=int, default=5005)
parser.add_argument('--buf', type=int, help='UDP buffer size', default=1024)
parser.add_argument(
    "--reuse", "-r", action="store_true", help="Set SO_REUSEADDR on socket"
)
parser.add_argument(
    "--echo", "-e", action="store_true", help="Echo the message back after receiving"
)
args = parser.parse_args()

UDP_IP = args.addr
UDP_PORT = args.port

sock = None
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP

    if args.reuse:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((UDP_IP, UDP_PORT))

    print("Listening on {}:{}".format(UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(args.buf)
        print(datetime.datetime.now(), "from:", addr)
        print(repr(data))
        if args.echo:
            prefix = platform.uname()[1].encode() + b" echoing: "
            print("Sending back:", prefix + data)
            sock.sendto(prefix + data, addr)
        if data == b"bye":
            print("Exit command issued.")
            break
finally:
    sock.close()
