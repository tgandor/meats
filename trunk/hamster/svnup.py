#!/usr/bin/env python
import os, urllib, re
from e import down, get

URL = 'https://meats.googlecode.com/svn/trunk/hamster/'

# chdir to 'working copy'
os.chdir(os.path.dirname(os.path.abspath(__file__)))

for f in re.findall('href="([^.][^"]+)"', get(URL)):
    if f.startswith('http') or f=='svnup.py':
        continue
    data = get(URL+f)
    if os.path.exists(f):
        old_data = open(f).read()
        if data != old_data:
            try:
                open(f, 'wb').write(data)
                print 'U\t%s' % f
            except:
                print 'Problem updating:', f
        else:
            print '\t%s - up to date.' % f
    else:
        try:
            open(f, 'wb').write(data)
            print 'A\t%s' % f
        except:
            print 'Problem creating:', f
