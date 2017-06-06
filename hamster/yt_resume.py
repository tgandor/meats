#!/usr/bin/env python

# install youtube_dl from pip

import androidhelper
import os
import glob
import time

target = '/mnt/sdcard/Download'

os.chdir(target)
pending = glob.glob('*.part')
if not pending:
    print('---\nNo pending files.')
    exit()
print('---\nFound {} pending files:\n---'.format(len(pending)))
print('\n---\n'.join(pending))

os.system('df .')

start = time.time()
print('Importing youtube_dl...')
import youtube_dl
print('Done in {:.1f} s'.format(time.time() - start))

android = androidhelper.Android()

for pending_file in pending:
    the_url = pending_file[:-5]
    filename, _ = os.path.splitext(the_url)
    the_url = filename[-11:]
    print('---\nTo download: {}\n---'.format(the_url))
    if not os.fork():
        youtube_dl.main(['--no-check-certificate', the_url])
    os.wait()

    os.system('df .')
    android.vibrate(1000)
    print('---')

