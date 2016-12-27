#!/usr/bin/env python

from __future__ import print_function

import sys
import threading
import time

def bug():
    while True:
        time.sleep(3)
        print('Waiting for your answer...')


if sys.version_info.major > 2:
    raw_input = input

thread = threading.Thread(target=bug)
thread.setDaemon(True)
thread.start()

data = raw_input('Enter something (considerately): ')
print('You entered:', data)
