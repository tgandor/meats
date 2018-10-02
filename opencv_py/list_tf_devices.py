#!/usr/bin/env python

from tensorflow.python.client.device_lib import list_local_devices

devices = list_local_devices()

print('-' * 79)
print('Done listing devices')
print('-' * 79)

for device in devices:
    print(device)
    print('-' * 79)

