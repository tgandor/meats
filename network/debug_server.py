#!/usr/bin/env python

from socket import *
from select import select

import os

timeout = 0.5
ctr = 0

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 12345))
s.settimeout(timeout)
s.listen(5)

clients = []

try:
    while True:
        try:
            csocket, addr = s.accept()
            print "Accepted conenction from", repr(addr)
            data = []
            data.append("Hello, world to %s on port %d\r\n\r\n" % addr)

            #data.append("You may want to see the environment variables:\r\n" +
            #    '-'*40+"\r\n\r\n%s\r\n" % os.popen('set').read().replace('\n','\r\n'))
            csocket.sendall("".join(data))
            csocket.setblocking(1)
            clients.append(csocket)
            print clients
	except KeyboardInterrupt:
            print "Ok, bye"
            break
        except:
            ctr += 1
            if ctr % int(5.0/timeout)  == 0:
                ctr = 0
                print "Nothing interesting for 5 seconds..."
        if len(clients):
            incoming, _, _ = select(clients, clients, clients, timeout)
            print "incoming: ", incoming
        else:
            incoming = []
        to_send = []
        for csocket in incoming:
            data = csocket.recv(256)
            if data == '':
                print "Client disconnected"
                csocket.shutdown(SHUT_RDWR)
                csocket.close()
                clients.remove(csocket)
            print "Received", data, map(ord, data)
            to_send.append("Did you say: "+data.strip()+"?\r\n")
        for msg in to_send:
            for csocket in clients:
                csocket.sendall(msg)

finally:
    for csocket in clients:
        csocket.shutdown(SHUT_RDWR)
        csocket.close()
    s.close()
