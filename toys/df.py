#!/usr/bin/env python

import os
import sys


def used_free(path):
    st = os.statvfs(path)
    return 4 * (st.f_blocks - st.f_bfree), 4 * st.f_bavail


human = False
if '-h' in sys.argv:
    human = True
    sys.argv.pop(sys.argv.index('-h'))

if len(sys.argv) < 2:
    print("Usage: {} [-h] PATH...".format(sys.argv[0]))
    exit()

data = []

for path in sys.argv[1:]:
    data += list(used_free(path))

if human:
    print(' '.join('{:,}'.format(num) for num in data))
else:
    print('\t'.join(str(num) for num in data))
