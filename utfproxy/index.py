#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()
import os
import urllib2
import sys
import re

requested = os.getenv("PATH_INFO") or '/'
iso = re.compile('iso-8859-2', re.I)

try:
    base = open('config.ini').read().strip()
except:
    print "Content-type: text/plain"
    print
    print "Error: create a file config.ini with the base server URL as only content."
    exit()
    
url = base + requested
resp = urllib2.urlopen(urllib2.Request(url))
contype = resp.info()['Content-Type']
del resp.info()['transfer-encoding']



if contype.startswith('text/html'):
    data = resp.read()
    data = data.replace('URL=/', 'URL=')
    # data = data.replace('iso-8859-2', 'UTF-8')
    data = iso.sub('UTF-8', data)
    print resp.info()
    sys.stdout.write(data.decode('ISO-8859-2').encode('UTF-8'))
else:
    print resp.info()
    sys.stdout.write(resp.read())

"""
print "Content-type: text/plain"
print
print "Hi, there"
print resp.info()
print dir(resp.info())
print resp.info().dict

"""
