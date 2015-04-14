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

the_url = androidhelper.Android().getClipboard().result

the_url = the_url.split()[-1]

if __name__ == '__main__':
    youtube_dl.main([the_url])
