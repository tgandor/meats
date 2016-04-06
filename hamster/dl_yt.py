#!/usr/bin/env python

# install youtube_dl and fake ctypes in lib/python2.7/site-packages

import os
import youtube_dl
import androidhelper

target = '/mnt/sdcard/Download'
print "trying to retrieve from clipboard"

try:
    os.chdir(target)
except:
    print 'failed chdir', target

print 'working in', os.getcwd()

android = androidhelper.Android()
the_url = android.getClipboard().result
the_url = the_url.split()[-1]
youtube_dl.main([the_url])
android.vibrate(2000)
