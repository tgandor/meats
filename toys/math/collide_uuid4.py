#!/usr/bin/env python

from __future__ import print_function

import sys
import uuid
import time

limit = int(sys.argv[1]) if len(sys.argv) > 1 else 8

seen = set()
start = time.time()
i = 0

while True:
    guid = str(uuid.uuid4())[:limit]
    if guid in seen:
        break
    seen.add(guid)
    # if len(seen) % 10**5 == 0:
    i += 1
    if i % 10**5 == 0:
        print('{:,} tries so far...'.format(len(seen)))
        sys.stdout.flush()

print('You did it. Found collision: {} in a set of {:,}.'.format(
    guid, len(seen)
))
