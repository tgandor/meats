#!/usr/bin/env python

# install youtube_dl and fake ctypes in lib/python2.7/site-packages

import androidhelper
import atexit
import os
import youtube_dl

target = '/mnt/sdcard/Download'
print "trying to retrieve from clipboard"

try:
    os.chdir(target)
except:
    print 'failed chdir', target
print 'working in', os.getcwd()
os.system('df .')

android = androidhelper.Android()
the_url = android.getClipboard().result
the_url = the_url.split()[-1]

def after_download():
    # module has no member 'statvfs'
    '''
    stats = os.statvfs(os.getcwd())
    print 'Done. {0:,} KB free ({1:.1f}%) left on device. ({2:,} KB total)'.format(
            stats.f_bavail * stats.f_bsize / 1024,
            100.0 * stats.f_bavail / stats.f_blocks,
            stats.f_blocks * stats.f_bsize / 1024
    )
    '''
    os.system('df .')
    android.vibrate(2000)

atexit.register(after_download)
youtube_dl.main([the_url])
