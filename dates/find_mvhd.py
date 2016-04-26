#!/usr/bin/env python

import sys


def process(f):
    i = 2
    finput = open(f)
    data = finput.read(2**i)
    while True:
        data += finput.read(2**i)
        i += 1
        if 'mvhd' in data:
            print("{} : 2**{} ({:,}) - found mvhd at {:,}".format(f, i, 2**i, data.find('mvhd')))
            break
        if len(data) < 2**i:
            print("{} : At {:,} - not found found 2**{} ({:,})".format(f, len(data), i, 2**i))
            break

if __name__ == '__main__':
    map(process, sys.argv[1:])
