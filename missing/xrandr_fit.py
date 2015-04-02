#!/usr/bin/env python

import os
import re
import sys


def get_resolutions():
    devices = []
    resolutions = []
    names = []

    for line in os.popen('xrandr').read().split('\n'):
        if line.find('connected') != -1:
            if resolutions:
                devices.append(resolutions)
                resolutions = []
            elif len(names):
                names.pop()
            names.append(line.split()[0])
            continue
        m = re.match('\s+(\d+)x(\d+)', line)
        if m:
            resolutions.append((
                int(m.group(1)),
                int(m.group(2)),
            ))

    if resolutions:
        devices.append(resolutions)
        resolutions = []

    return zip(names, devices)

if __name__ == '__main__':
    for name, resolutions in get_resolutions():
        print name
        for res in sorted(resolutions, key=lambda x: -x[0]*x[1]):
            print '%10d' % (res[0]*res[1],), res
