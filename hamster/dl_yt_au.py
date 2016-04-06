#!/usr/bin/env python

# install youtube_dl and fake ctypes in lib/python2.7/site-packages

import os
import youtube_dl
import androidhelper

print "trying to retrieve from clipboard"

try:
    os.chdir('/mnt/sdcard/Download')
except:
    print 'failed chdir /mnt/sdcard/Download'

print 'working in', os.getcwd()

android = androidhelper.Android()
the_url = android.getClipboard().result
the_url = the_url.split()[-1]
youtube_dl.main(['--format', 'm4a', the_url])
android.vibrate(2000)
