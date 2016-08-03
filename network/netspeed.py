#!/usr/bin/env python

import os
import sys
import time
import re

if len(sys.argv) < 2:
    print "Usage: %s IFACE" % sys.argv[0]
    exit()

interface = sys.argv[1]

def get_bytes():
    data = os.popen('ifconfig '+interface).read()
    m = re.search("RX bytes:(\d+)", data)
    rxb = int(m.group(1))
    m = re.search("TX bytes:(\d+)", data)
    txb = int(m.group(1))
    return rxb, txb

try:
    rxb0, txb0 = get_bytes()
except Exception, e:
    print "Error getting data (see other messages)"
    exit()

print "If you see this, it's working. Exit with Ctrl-C."

def human_format(n):
    if n > 2**20:
        return "%6.1f MB" % (n/2.0**20,)
    if n > 2**10:
        return "%6.1f KB" % (n/2.0**10,)
    return "%6d B " % n

idle_secs = 0
maxtx, maxrx = 0, 0

while True:
    try:
        time.sleep(1)
    except:
        print
        break

    try:
        rxb, txb = get_bytes()
    except:
        print "Error retrieving data, quitting!"
        break

    if (rxb, txb) == (rxb0, txb0):
        idle_secs += 1
        if idle_secs % 10 == 0:
            print "%d seconds idle" % idle_secs
        continue
    else:
        idle_secs = 0
    print "Recv %s/s, Send %s/s. Total: %s, %s." % tuple(
            map(human_format, (rxb-rxb0, txb-txb0, rxb, txb)))
    maxtx = max(maxtx, txb-txb0)
    maxrx = max(maxrx, rxb-rxb0)
    rxb0, txb0 = rxb, txb

print "Bye, max speeds were: %s/s, %s/s." % (
                human_format(maxrx), human_format(maxtx))
