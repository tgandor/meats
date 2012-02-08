#!/usr/bin/env python

import sys
import os
import re
import time
import urllib
import random

urllib.URLopener.version = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'

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
    print 'Retrieving from the Web'
    content = urllib.urlopen(url).read()
    open(url_file, 'wb').write(url)
    open(content_file, 'wb').write(content)
    return content

def get_audio(hostname, audio_id):
    ts = int(time.time() * 1000)
    url = "http://%s/Audio.ashx?id=%s&type=2&tp=mp3&ts=%d" % (hostname,
            audio_id, ts)
    return urllib.urlopen(url).read()

def deutf(starred):
    starred = starred.group()
    ords = [ starred[i:i+2]  for i in xrange(1, len(starred), 3) ]
    starred = ''.join( chr(int(o, 16)) for o in ords )
    return starred.decode('utf-8').encode(sys.getfilesystemencoding())

def clean_name(dirty):
    dirty = re.sub('(\\*[0-9a-fA-F]{2})+', deutf, dirty)
    return dirty.replace('+','_')

if not os.path.exists('.hamster'):
    print 'Missing .hamster directory, creating...'
    os.mkdir('.hamster')

if len(sys.argv) < 2:
    print 'Usage: %s [URL]' % sys.argv[0]


the_url = sys.argv[1]
hostname = re.match('http://([^/]+)/', the_url).group(1)
hostpath = re.match('http://[^/]+(/.*)', the_url).group(1)
content = get_content(the_url)

page = 2
while True:
    nextpage = "%s,%d" % (hostpath, page)
    if content.find(nextpage) == -1:
        break
    print "Extra page: ", nextpage
    content += get_content("%s,%d" % (the_url, page))
    page += 1

dirname = clean_name(the_url[the_url.rfind('/')+1:])
if not os.path.exists(dirname):
    print "Creating directory: "+dirname
    os.mkdir(dirname)
else:
    print "Directory %s seems to already exist." % dirname

print "Starting download loop, exit easily with Ctrl-C while sleeping."

for title, audio_id in sorted(set(re.findall('/([^/]+),(\d+)\\.mp3', content))):
    title_c = clean_name(title)+'.mp3'
    filename = os.path.join(dirname, title_c)
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        print ">%s< seems to exist, skipping." % filename
        continue
    print "Retrieving >%s< (id: %s)" % (title_c, audio_id)
    open(filename, 'wb').write(get_audio(hostname, audio_id))
    print "Sleeping..."
    time.sleep(random.random()*10)

