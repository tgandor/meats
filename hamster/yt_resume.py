#!/usr/bin/env python

# install youtube_dl from pip

import androidhelper
import atexit
import os
import youtube_dl
import glob

target = '/mnt/sdcard/Download'

os.chdir(target)
pending = glob.glob('*.part')
if not pending:
    print('---\nNo pending files.')
    exit()
print('---\nFound {} pending files:\n---'.format(len(pending)))
print('\n---\n'.join(pending))

the_url = pending[0][:-5]
filename, _ = os.path.splitext(the_url)
the_url = filename[-11:]
print('---\nTo download: {}\n---'.format(the_url))

android = androidhelper.Android()
os.system('df .')
print('---')


def after_download():
    # os module has no member 'statvfs'
    os.system('df .')
    android.vibrate(2000)

atexit.register(after_download)
youtube_dl.main([the_url])
