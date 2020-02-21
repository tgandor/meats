#!/usr/bin/env python

import sys

with open(sys.argv[1], 'rb') as f:
    while True:
        c = ord(f.read(1))
        if c == 0xff:
            d = ord(f.read(1))
            if d == 0xd8:
                print('SOI', '@', f.tell())
                continue
            if d == 1:
                print('TEM', '@', f.tell())
                continue
            if 0xd0 <= d <= 0xd7:
                print('RST', d-0xd0, '@', f.tell())
                continue
            if d == 0xd9:
                print('EOI', '@', f.tell())
                break
            if d == 0:
                # print('FF00 - not a marker', f.tell())
                continue

            h = ord(f.read(1))
            l = ord(f.read(1))
            size = 256 * h + l
            data = f.read(size - 2)  # 2 bytes already there

            if d == 0xc0: # SOF 0
                print('SOF', 'size:', size, '@', f.tell(), 'data:', data)
                continue

            print(hex(c), hex(d), 'size:', size, '@', f.tell())
