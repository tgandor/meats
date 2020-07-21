#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

import datetime
import os
import sys
import time
import re

if len(sys.argv) < 2:
    print("Usage: %s IFACE [INTERVAL]" % sys.argv[0])
    exit()

interval = 1
max_idle = 600
interface = sys.argv[1]

if len(sys.argv) > 2:
    interval = int(sys.argv[2])


def get_bytes():
    data = os.popen('ifconfig '+interface).read()
    m = re.search(r"RX (?:packets \d+\s*)bytes(?::? *)(\d+)", data)
    rxb = int(m.group(1))
    m = re.search(r"TX (?:packets \d+\s*)bytes(?::? *)(\d+)", data)
    txb = int(m.group(1))
    return rxb, txb


try:
    rxb0, txb0 = get_bytes()
except Exception as e:
    print("Error getting data (see other messages)")
    print(e)
    exit()

print("If you see this, it's working. Exit with Ctrl-C.")
sys.stdout.flush()


def human_format(n, mb=True):
    if n > 2**20 and mb:
        return "{:8,.1f} MB".format(n/2**20)
    if n > 2**10:
        return "{:8,.1f} KB".format(n/2**10)
    return "%8d B " % n


class Blinker:
    def __init__(self):
        self.last_status = 0  # success

    def on(self):
        if self.last_status == 0:
            self.last_status = os.system('xset led 3')

    def off(self):
        if self.last_status == 0:
            self.last_status = os.system('xset -led 3')


blinker = Blinker()
idle_secs = 0
maxtx, maxrx = 0, 0
prev_rxb, prev_txb = rxb0, txb0
next_report = interval
started = datetime.datetime.now()

while True:
    try:
        time.sleep(interval)
        blinker.off()
    except:
        print()
        break

    try:
        rxb, txb = get_bytes()
    except:
        print("Error retrieving data, quitting!")
        break

    if (rxb, txb) == (prev_rxb, prev_txb):
        idle_secs += interval
        if idle_secs == next_report:
            print(time.strftime('%H:%M:%S') + " %d seconds idle" % idle_secs)
            sys.stdout.flush()
            if next_report < max_idle:
                next_report *= 2
            else:
                next_report += max_idle
        continue
    else:
        if idle_secs > 0:
            print(time.strftime('%H:%M:%S') + " resume after %d seconds" % idle_secs)
        idle_secs = 0
        next_report = interval
    blinker.on()
    duration = datetime.datetime.now() - started
    print("{} Recv {}, Send {}. Session ({}): Rx {}, Tx {}, avg: {}/s, {}/s.".format(
        time.strftime('%H:%M:%S'),
        human_format(rxb - prev_rxb, False),
        human_format(txb - prev_txb, False),
        '{}'.format(duration).split('.')[0],
        human_format(rxb - rxb0),
        human_format(txb - txb0),
        human_format((rxb - rxb0) // duration.seconds),
        human_format((txb - txb0) // duration.seconds),
    ))
    sys.stdout.flush()
    maxtx = max(maxtx, txb - prev_txb)
    maxrx = max(maxrx, rxb - prev_rxb)
    prev_rxb, prev_txb = rxb, txb

print("Bye, max speeds were: {}/s, {}/s.".format(
    human_format(maxrx/interval), human_format(maxtx/interval)
))
