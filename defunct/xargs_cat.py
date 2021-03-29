#!/usr/bin/env python

import os
import shutil
import sys

separator = '\n{0}\n'.format(sys.argv[1]) if len(sys.argv) > 1 else ''

for filename in sys.stdin:
    filename = filename.strip()
    if os.path.exists(filename):
        sample = open(filename).read(1024)
        if not sample.strip():
            sys.stderr.write('{1}: File `{0}` seems empty\n'.format(filename, sys.argv[0]))
            continue
        f = open(filename)
        bom = f.read(3)
        if bom == '\xef\xbb\xbf':
            sys.stderr.write('{1}: File `{0}` bom: {2}\n'.format(filename, sys.argv[0], repr(bom)))
        else:
            sys.stdout.write(bom)
        shutil.copyfileobj(f, sys.stdout)
        f.close()
        sys.stdout.flush()
        sys.stdout.write(separator)
    else:
        sys.stderr.write('{1}: File `{0}` not found\n'.format(filename, sys.argv[0]))
