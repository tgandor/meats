#!/usr/bin/env python
from __future__ import unicode_literals

import sys

if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(path))

import youtube_dl

import androidhelper
print "trying to retrieve from clipboard"
'''
try:
	os.chdir('/mnt/extSdCard/Music')
except:
    print 'failed chdir /mnt/extSdCard/Music'
'''

try:
    os.chdir('/mnt/sdcard/Download')
except:
    print 'failed chdir /mnt/sdcard/Download'

print 'working in', os.getcwd()

the_url = androidhelper.Android().getClipboard().result

the_url = the_url.split()[-1]

# ignoring hacks:
sys.stderr.isatty = lambda: False
sys.stderr.flush = lambda: None

if __name__ == '__main__':
    youtube_dl.main([the_url])
