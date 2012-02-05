#!/usr/bin/env python

import sys
import os

def get_content(url):
    from hashlib import md5
    digest = md5(url).hexdigest()
    url_file = os.path.join('.hamster/', digest+'.url')
    content_file = os.path.join('.hamster', digest+'.data')
    if os.path.exists(url_file):
        print 'Retrieving from cache'
        saved_url = open(url_file).read()
        if saved_url != url:
            print "You're lucky! Found a md5 collision between:\n%s\nand:\n%s" % (saved_url, url)
        return open(content_file).read()
    import urllib
    urllib.URLopener.version = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'
    print 'Retrieving from the Web'
    content = urllib.urlopen(url).read()
    open(url_file, 'w').write(url)
    open(content_file, 'w').write(content)
    return content

if not os.path.exists('.hamster'):
    print 'Missing .hamster directory, creating...'
    os.mkdir('.hamster')

if len(sys.argv) < 2:
    print 'Usage: %s [URL]' % sys.argv[0]


the_url = sys.argv[1]
content = get_content(the_url)

