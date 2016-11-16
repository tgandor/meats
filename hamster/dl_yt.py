#!/usr/bin/env python

import androidhelper
import atexit
import os
import youtube_dl

target = '/mnt/sdcard/Download'

try:
    os.chdir(target)
except:
    print 'failed chdir', target
os.system('df .')

android = androidhelper.Android()

if not android.checkWifiState().result:
    print('Not on WiFi, exiting.')
    exit()

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
