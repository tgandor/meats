#!/usr/bin/env python

from ctypes import *
rt = CDLL('librt.so')
CLOCK_REALTIME = 0

class timespec(Structure):
     _fields_ = [("tv_sec", c_long), ("tv_nsec", c_long)]

res = timespec()
rt.clock_getres(CLOCK_REALTIME, byref(res))

print('Period {} s, {} ns'.format(res.tv_sec, res.tv_nsec))
SYSTEM_HZ = round(1/(res.tv_sec + (res.tv_nsec/10.0**9)))
print('Period {} Hz'.format(SYSTEM_HZ))
