#!/usr/bin/env python

from glob import *
from os import *
from shutil import *

ASK_EVERY = False
FILES_PATTERN = '*.mp3'

if __name__=='__main__':
    for d in sorted(glob('*/')):
        for f in glob(d+path.sep+FILES_PATTERN):
            ret = system('mplayer "%s"' % f)
            if ret <> 0 or ASK_EVERY:
                if raw_input('ditch dir %s (y/N)? ' % d)=='y':
                    rmtree(d)
                    break
            if ret <> 0:
                if raw_input('quit (y/N)? ')=='y':
                    print "bye."
                    exit()
