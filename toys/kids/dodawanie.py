#!/usr/bin/env python

import random
import re
import sys

try:
    LIMIT=int(sys.argv[1])
except:
    LIMIT=10

points = 0

while True:
    a = random.randint(1, LIMIT)
    b = random.randint(1, LIMIT)
    while True:
        try:
            ans = raw_input('%d + %d = ? ' % (a, b))
            c = int(ans)
            break
        except EOFError:
            print '\nDo widzenia'
            exit()
        except ValueError:
            print 'Nie rozumiem: "%s"' % (ans,)
    if c == a + b:
        points += 1
        print 'Dobrze! Twoje punkty:', points
    else:
        print 'Niedobrze... to jest: %d' % (a+b,)

