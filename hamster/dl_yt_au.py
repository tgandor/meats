from __future__ import print_function

import androidhelper
import atexit
import os

target = os.path.dirname(__file__) + '/../../Download'

try:
    os.chdir(target)
except OSError:
    print('failed changing directory:', target)
    exit()

os.system('df .')

android = androidhelper.Android()

if not android.checkWifiState().result:
    print('Not on WiFi, exiting.')
    exit()

the_url = android.getClipboard().result
the_url = the_url.split()[-1]


def after_download():
    os.system('df .')
    android.vibrate(2000)

atexit.register(after_download)

print('Starting download of: ' + the_url)
import youtube_dl
youtube_dl.main([
    '--no-check-certificate',
    '--format', 'm4a',
    the_url
    ])
