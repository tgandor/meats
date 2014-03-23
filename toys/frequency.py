#!/usr/bin/env python

import time

print 'Keep pressing <Enter> or enter something to quit.'

last_hit = time.time()
line = ''

while line == '':
    line = raw_input()
    hit = time.time()
    delay = hit - last_hit
    print '%6.2f ms, %3.2f Hz (FPS), pulse %2.1f (RPM)' % (delay * 1000, 1/delay, 60/delay)
    last_hit = hit

print 'Bye!'
