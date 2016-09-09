#!/usr/bin/env python

import os
import qrcode
import sys

target = '/mnt/sdcard/DCIM'


def get_data():
    print "trying to retrieve from clipboard"
    try:
        import androidhelper
        android = androidhelper.Android()
        return android.getClipboard().result
    except ImportError:
        return sys.argv[1]


try:
    os.chdir(target)
except:
    print 'failed chdir', target
print 'working in', os.getcwd()

img = qrcode.make(get_data())
img.convert('RGB').save('qr_code.png')
