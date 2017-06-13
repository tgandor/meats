#!/usr/bin/env python
from __future__ import print_function
import sys


def parse_angle(data):
    factor = 1.0
    result = 0.0
    for chunk in data.split(':'):
        result += factor * float(chunk)
        factor /= 60.0
    return result


def to_dms(angle):
    d = int(angle)
    rest = angle - d
    m = int(rest * 60)
    rest -= m / 60.0
    s = rest * 3600
    return "%d:%d:%.2f" % (d, m, s)


if len(sys.argv) != 2:
    print("Usage:")
    print("  %s angle1[,angle2]                 - angle given as float in degrees" % sys.argv[0])
    print("  %s deg:M:S.sss[,deg:M:S.sss]       - angle given as degrees:minutes:seconds" % sys.argv[0])
    print("  %s -                               - read angle(s) from standard input" % sys.argv[0])
    exit()

if sys.argv[1] == '-':
    data = sys.stdin.readline().strip()
else:
    data = sys.argv[1]

angles = list(map(parse_angle, data.split(',')))
print(','.join(map(str, angles)))
print(','.join(map(to_dms, angles)))
