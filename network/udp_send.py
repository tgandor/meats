#!/usr/bin/env python

from __future__ import print_function
import argparse
import socket
import sys

parser = argparse.ArgumentParser()
parser.add_argument('message', help='String to broadcast', default='Where RU?', nargs='?')
parser.add_argument('--addr', default='255.255.255.255', help='IP to send to, may be broadcast')
parser.add_argument('--port', default=5005, help='Target UDP port to send to')
parser.add_argument('--listen', '-l', action='store_true', help='Listen for replies after broadcast')
parser.add_argument('--timeout', '-t', type=float, help='Socket operation timeout', default=10.0)
args = parser.parse_args()

UDP_IP = args.addr
UDP_PORT = args.port
MESSAGE = args.message.encode()

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = None
try:
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    broken_global = (UDP_IP == '255.255.255.255' and sys.platform.startswith('win'))

    if not broken_global:
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    else:
        print('Sorry, but 255.255.255.255 is broken on Windows.')
        import netifaces
        for interface in netifaces.interfaces():
            for ipv4 in netifaces.ifaddresses(interface).get(netifaces.AF_INET, []):
                UDP_IP = ipv4['broadcast']
                print('Broadcasting instead to', UDP_IP)
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    if args.listen:
        sock.settimeout(args.timeout)
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                print('Reply from {}: {}'.format(addr, data))
            except socket.timeout:
                print('Timeout ({} s) reached.'.format(args.timeout))
                break
finally:
    if sock is not None:
        sock.close()
