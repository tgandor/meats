#!/usr/bin/env python

from __future__ import print_function

import argparse
import socket
from select import select

parser = argparse.ArgumentParser()
parser.add_argument('--address', '-a', help='IPv4 address to bind to', default='')
parser.add_argument('port', type=int, nargs='?', help='Port to bind to', default=12345)
parser.add_argument('--timeout', '-t', type=float, help='Socket timeout', default=0.5)
parser.add_argument('--quiet', '-q', action='store_true', help='Less verbose operation')
args = parser.parse_args()

quiet = False

ctr = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((args.address, args.port))
s.settimeout(args.timeout)
s.listen(5)

clients = []

try:
    while True:
        try:
            client_socket, addr = s.accept()
            print('Accepted connection from', repr(addr))
            client_socket.sendall(('Hello, world to %s on port %d\r\n\r\n' % addr).encode())
            client_socket.setblocking(1)
            clients.append(client_socket)
            print(clients)
        except KeyboardInterrupt:
            print('Ok, bye')
            break
        except socket.timeout:
            ctr += 1
            if ctr % int(5.0/args.timeout) == 0:
                ctr = 0
                print('Nothing interesting for 5 seconds...')
        if len(clients):
            incoming, _, _ = select(clients, clients, clients, args.timeout)
            print('incoming: ', incoming)
        else:
            incoming = []
        to_send = []
        for client_socket in incoming:
            data = client_socket.recv(256)
            if data == b'':
                print('Client disconnected')
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
                clients.remove(client_socket)
            print('Received', data)
            to_send.append('Did you say: ' + data.decode().strip() + '?\r\n')
        for msg in to_send:
            for client_socket in clients:
                client_socket.sendall(msg.encode())

finally:
    for client_socket in clients:
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
    s.close()
