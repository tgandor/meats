#!/usr/bin/env python

from math import sqrt

while True:
    data = map(int, raw_input().split())
    a, b, c = data[:3]
    if a >= b+c or b >= a+c or c >= a+b:
        print 'Not a triangle.'
        continue
    print 'Area %.3f, perimeter: %d' % ( sqrt( (a+b+c) * (a+b-c) * (a-b+c) * (-a+b+c) ) / 4, a+b+c)
