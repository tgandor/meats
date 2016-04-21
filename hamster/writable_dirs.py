#!/usr/bin/env python

import os
import sys
import tempfile
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

def test_file_write(directory):
    try:
        _, temp_path = tempfile.mkstemp(dir=directory)
        os.remove(temp_path)
        return True
    except:
        return False

    
if __name__ == '__main__':
    for d in recurse('/'):
        if test_file_write(d):
            print(d + " OK")
        else:
            print(d + " FAIL")
        
