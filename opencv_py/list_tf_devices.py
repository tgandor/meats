#!/usr/bin/env python

import os
import sys
from tensorflow.python.client.device_lib import list_local_devices

if len(sys.argv) > 1:
    if sys.argv[1] in '--help':
        print('Usage: {} [CUDA_VISIBLE_DEVICES]'.format(sys.argv[0]))
        exit()
    os.environ['CUDA_VISIBLE_DEVICES'] = sys.argv[1]

devices = list_local_devices()

print('-' * 79)
print('Done listing devices')
print('-' * 79)

for device in devices:
    print(device)
    print('-' * 79)

