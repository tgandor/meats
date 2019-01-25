#!/usr/bin/env python

import re
import sys

decimals = 3
if len(sys.argv) > 1:
    decimals = int(sys.argv[1])

data = sys.stdin.read()

result, count = re.subn(r'\d+\.\d{4,}', lambda x: x.group()[:x.group().index('.') + decimals + 1], data)

sys.stdout.write(result)
sys.stderr.write('{} floats shortened\n'.format(count))
