#!/usr/bin/env python
import sys

if len(sys.argv) != 2:
    print "Usage:"
    print "  %s angle1[,angle2]" % sys.argv[0]
    print "  %s deg:M:S.sss[,deg:M:S.sss]" % sys.argv[0]
    exit()

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

angles = map(parse_angle, sys.argv[1].split(','))
print ','.join(map(str, angles))
print ','.join(map(to_dms, angles))
