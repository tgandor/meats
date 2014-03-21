#!/usr/bin/env python
import os, urllib, re
from e import down, get

URL = 'https://meats.googlecode.com/svn/trunk/hamster/'

for f in re.findall('href="([^.][^"]+)"', get(URL)):
    if not f.startswith('http'):
        data = get(URL+f)
        if os.path.exists(f):
            old_data = open(f).read()
            if data != old_data:
                open(f, 'rb').write(data)
                print 'U\t%s' % f
            else:
                print '\t%s - up to date.' % f
        else:
            open(f, 'rb').write(data)
            print 'A\t%s' % f
