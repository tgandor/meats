#!/usr/bin/env python

import os
import sys
import time


next_check = time.time() + 5
max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 4


def recurse(root, level=0):
    global next_check
    if time.time() > next_check:
        sys.stderr.write(' ... processing: '+root+'\n')
        next_check += 5
    if os.access(root, os.W_OK | os.X_OK):
        yield root
    elif os.access(root, os.R_OK | os.X_OK) and root not in ['/proc', '/sys', '/usr/share/doc'] and level < max_depth:
        for subdir in filter(os.path.isdir, (os.path.join(root, leaf) for leaf in os.listdir(root))):
            for writeable in recurse(subdir, level+1):
                yield writeable

if __name__ == '__main__':
    map(sys.stdout.write, (_+'\n' for _ in recurse('/')))
