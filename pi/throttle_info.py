#!/usr/bin/env python

'''
https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=147781&start=50#p972790
Supposed meanings of get_throttled value bits.
'''

import os
from collections import OrderedDict as odict

description = """
0: under-voltage
1: arm frequency capped
2: currently throttled 
16: under-voltage has occurred
17: arm frequency capped has occurred
18: throttling has occurred
""".strip()

bits = odict()
for line in description.split('\n'):
    bit, flag_description = line.split(':')
    bits[int(bit)] = flag_description

out = os.popen('vcgencmd get_throttled').read().strip()
print(out)
val = int(out.split('=')[1], 16)
print(val)
print('-'*32)
print(''.join('%-4d' % i for i in range(0, 32, 4)))
print('-'*32)
bit_string = bin(val)[:1:-1]
if len(bit_string) < 32:
    bit_string += '0' * (32 - len(bit_string))
print(bit_string)

for key, val in bits.items():
    if bit_string[key] == '1':
        print('Bit {}: {}'.format(key, val))

