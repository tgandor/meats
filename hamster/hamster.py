#!/usr/bin/env python

import sys
import os
import re
import time
import urllib
import random

urllib.URLopener.version = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0'

def get_content(url):
    if not os.path.exists('.hamster'):
        print 'Missing .hamster directory, creating...'
        os.mkdir('.hamster')
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

def clean_name(dirty):
    def deutf(starred):
        starred = starred.group()
        ords = [ starred[i:i+2]  for i in xrange(1, len(starred), 3) ]
        starred = ''.join( chr(int(o, 16)) for o in ords )
        return starred.decode('utf-8').encode(sys.getfilesystemencoding())
    dirty = re.sub('(\\*[0-9a-fA-F]{2})+', deutf, dirty)
    return dirty.replace('+','_')

class MusicHandler(object):
    pattern = re.compile('/([^/]+),(\d+)\\.mp3')
    fileext = '.mp3'
    def get_data(self, hostname, file_id):
        ts = int(time.time() * 1000)
        url = "http://%s/Audio.ashx?id=%s&type=2&tp=mp3&ts=%d" % (hostname, file_id, ts)
        return urllib.urlopen(url).read()

class MusicHandler(object):
    pattern = re.compile('/([^/]+),(\d+)\\.mp3')
    fileext = '.mp3'
    def get_data(self, hostname, file_id):
        ts = int(time.time() * 1000)
        url = "http://%s/Audio.ashx?id=%s&type=2&tp=mp3&ts=%d" % (hostname, file_id, ts)
        return urllib.urlopen(url).read()

class VideoHandler(object):
    pattern = re.compile('/([^/]+),(\d+)\\.(?:avi|mp4)')
    fileext = '.flv'
    def get_data(self, hostname, file_id):
        url = "http://%s/Video.ashx?id=%s&type=1&file=video" % (hostname, file_id)
        return urllib.urlopen(url).read()

def retrieve_all(hostname, handler, contents, targetdir):
    print "Starting download loop, exit easily with Ctrl-C while sleeping."
    # this is uglier than I wanted
    tasks = sorted(set(sum((handler.pattern.findall(content) for content in contents), [])))
    # but it gives all "tasks" in one sorted list
    for title, file_id in tasks:
        title_c = clean_name(title) + handler.fileext
        filename = os.path.join(targetdir, title_c)
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            print ">%s< seems to exist, skipping." % filename
            continue
        print "Retrieving >%s< (id: %s)" % (title_c, file_id)
        data = handler.get_data(hostname, file_id)
        if data.startswith("The page cannot be displayed"):
            print "Reading failed!"
        else:
            open(filename, 'wb').write(data)
        print "Sleeping..."
        time.sleep(random.random() * 8 + 2)

def main():
    if len(sys.argv) < 2:
        print 'Usage: %s [dl|ls|find] URL' % sys.argv[0]

    the_url = sys.argv[1]
    hostname = re.match('http://([^/]+)/', the_url).group(1)
    hostpath = re.match('http://[^/]+(/.*)', the_url).group(1)
    content = get_content(the_url)

    contents = [content[content.rfind('folderContentContainer'):]]

    page = 2
    while True:
        nextpage = "%s,%d" % (hostpath, page)
        if content.find(nextpage) == -1:
            break
        print "Extra page: ", nextpage
        content = get_content("%s,%d" % (the_url, page))
        contents.append(content[content.rfind('folderContentContainer'):])
        page += 1

    content = " ".join(contents)

    dirname = clean_name(the_url[the_url.rfind('/')+1:])
    if not os.path.exists(dirname):
        print "Creating directory: "+dirname
        os.mkdir(dirname)
    else:
        print "Directory %s seems to already exist." % dirname

    retrieve_all(hostname, MusicHandler(), contents, dirname)
    #retrieve_all(hostname, VideoHandler(), contents, dirname)

if __name__ == '__main__':
    main()
