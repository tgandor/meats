#!/usr/bin/env python

from __future__ import print_function

import socket
from select import select

import os
import sys

address = ''
port = 12345
quiet = False

timeout = 0.5
ctr = 0

try:
    port = int(sys.argv[1])
except:
    pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 12345))
s.settimeout(timeout)
s.listen(5)

clients = []

try:
    while True:
        try:
            csocket, addr = s.accept()
            print("Accepted conenction from", repr(addr))

            csocket.sendall(("Hello, world to %s on port %d\r\n\r\n" % addr).encode())

            csocket.setblocking(1)
            clients.append(csocket)
            print(clients)
        except KeyboardInterrupt:
            print("Ok, bye")
            break
        except socket.timeout:
            ctr += 1
            if ctr % int(5.0/timeout)  == 0:
                ctr = 0
                print("Nothing interesting for 5 seconds...")
        if len(clients):
            incoming, _, _ = select(clients, clients, clients, timeout)
            print("incoming: ", incoming)
        else:
            incoming = []
        to_send = []
        for csocket in incoming:
            data = csocket.recv(256)
            if data == b'':
                print("Client disconnected")
                csocket.shutdown(socket.SHUT_RDWR)
                csocket.close()
                clients.remove(csocket)
            print("Received", data, map(ord, data))
            to_send.append("Did you say: "+data.decode().strip()+"?\r\n")
        for msg in to_send:
            for csocket in clients:
                csocket.sendall(msg.encode())

finally:
    for csocket in clients:
        csocket.shutdown(socket.SHUT_RDWR)
        csocket.close()
    s.close()
