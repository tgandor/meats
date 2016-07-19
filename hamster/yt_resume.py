#!/usr/bin/env python

# install youtube_dl from pip

import androidhelper
import atexit
import os
import youtube_dl
import glob

target = '/mnt/sdcard/Download'
print('trying to retrieve from clipboard')

os.chdir(target)
pending = glob.glob('*.part')
if not pending:
    exit()
print('\n---\n'.join(pending))

the_url = pending[0][:-5]
filename, _ = os.path.splitext(the_url)
the_url = filename[-11:]
print('---\nTo download: {}\n---'.format(the_url))

android = androidhelper.Android()
os.system('df .')
print('---')

def after_download():
    # module has no member 'statvfs'
    """
    stats = os.statvfs(os.getcwd())
    print 'Done. {0:,} KB free ({1:.1f}%) left on device. ({2:,} KB total)'.format(
            stats.f_bavail * stats.f_bsize / 1024,
            100.0 * stats.f_bavail / stats.f_blocks,
            stats.f_blocks * stats.f_bsize / 1024
    )
    """
    os.system('df .')
    android.vibrate(2000)

atexit.register(after_download)
youtube_dl.main([the_url])
