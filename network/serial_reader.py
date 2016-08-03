#!/usr/bin/env python

import serial
import glob

port = glob.glob('/dev/ttyUSB*')[0]
baudrate = 460800
parity = serial.PARITY_NONE
rtscts = False
xonxoff = False

print("Using port: {}".format(port))

serial = serial.serial_for_url(port, baudrate, parity=parity, rtscts=rtscts, xonxoff=xonxoff, timeout=1)

while True:
    line = serial.readline()
    if line == b'':
        continue
    print('Line: {}'.format(repr(line)))
