#!/usr/bin/env python

import sys
import os
import re
import time
import urllib
import random
import cStringIO

urllib.URLopener.version = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0'

CHUNK = 512 * 1024

def human(x):
    for sufix in ['', 'K', 'M', 'G']:
        if x < 1024:
            return "%.1f %s" % (x, sufix)
        x /= 1024.0
    return "%.1f P" % x

def get_content(url):
    if not os.path.exists('.hamster'):
        print 'Missing .hamster directory, creating...'
        os.mkdir('.hamster')
    from hashlib import md5
    digest = md5(url).hexdigest()
    url_file = os.path.join('.hamster/', digest+'.url')
    content_file = os.path.join('.hamster', digest+'.data')
    if os.path.exists(url_file):
        print '  (retrieving from cache...)'
        saved_url = open(url_file).read()
        if saved_url != url:
            print "You're lucky! Found a md5 collision between:\n%s\nand:\n%s" % (saved_url, url)
        return open(content_file).read()
    print '  (retrieving from the Web...)'
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
    dirty = dirty.replace('(', '').replace(')', '')
    return dirty.replace('+','_')

def read_with_progress(resp):
    start = time.time()
    sio = cStringIO.StringIO()
    for chunk in iter(lambda: resp.read(CHUNK), ''):
        sio.write(chunk)
        sys.stdout.write('.')
        try:
            sys.stdout.flush()
        except:
            pass
    elap = time.time() - start
    print " done: %sB in %.1f s, %sB/s" % (human(sio.tell()), elap, human(sio.tell()/elap))
    return sio.getvalue()

def download_url(url):
    resp = urllib.urlopen(url)
    msg = resp.info()
    length = msg.getheader('Content-Length')
    if length:
        print "Downloading %sB " % human(int(length)),
    return read_with_progress(resp)

class MusicHandler(object):
    pattern = re.compile('/([^/]+),(\d+)\\.mp3')
    fileext = '.mp3'
    def get_data(self, hostname, file_id):
        ts = int(time.time() * 1000)
        url = "http://%s/Audio.ashx?id=%s&type=2&tp=mp3&ts=%d" % (hostname, file_id, ts)
        return download_url(url)

class VideoHandler(object):
    pattern = re.compile('/([^/]+),(\d+)\\.(?:avi|mp4)')
    fileext = '.flv'
    def get_data(self, hostname, file_id):
        url = "http://%s/Video.ashx?id=%s&type=1&file=video" % (hostname, file_id)
        return download_url(url)

def _extract_tasks(handler, contents):
    # this is uglier than I wanted
    # but it gives all "tasks" in one sorted list
    return sorted(set(sum((handler.pattern.findall(content) for content in contents), [])))

def retrieve_all(hostname, handler, contents, targetdir):
    print "Starting download loop, exit easily with Ctrl-C while sleeping."
    tasks = _extract_tasks(handler, contents)
    total = len(tasks)
    i = 0
    for title, file_id in tasks:
        title_c = clean_name(title) + handler.fileext
        filename = os.path.join(targetdir, title_c)
        i += 1
        print "%d/%d" % (i, total),
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

def _get_inner_content(the_url):
    content = get_content(the_url)
    pos = content.rfind('folderContentContainer')
    if pos == -1: # backward compatibility?
        return content
    return content[pos:]

def _gather_contents(the_url):
    hostpath = re.match('http://[^/]+(/.*)', the_url).group(1)
    contents = [_get_inner_content(the_url)]
    page = 2
    while True:
        nextpage = "%s,%d" % (hostpath, page)
        unquoted = urllib.unquote(nextpage)
        last = contents[-1]
        if last.find(nextpage)==-1 and last.find(unquoted)==-1:
            break
        print "Extra page: ", nextpage
        contents.append(_get_inner_content("%s,%d" % (the_url, page)))
        page += 1
    return contents

def command_dl(the_url):
    hostname = re.match('http://([^/]+)/', the_url).group(1)
    dirname = clean_name(the_url[the_url.rfind('/')+1:])
    if not os.path.exists(dirname):
        print "Creating directory: "+dirname
        os.mkdir(dirname)
    else:
        print "Directory %s seems to already exist." % dirname

    retrieve_all(hostname, MusicHandler(), _gather_contents(the_url), dirname)
    #retrieve_all(hostname, VideoHandler(), _gather_contents(the_url), dirname)

def _print_tasks(tasks, ext):
    if len(tasks) == 0:
        print " (empty)"

    fmt = "%%%dd. %%-%ds (id: %%s)" % (
        len(str(len(tasks))),
        max(len(t[0]) for t in tasks) + len(ext),
    )
    i = 1
    for title, file_id in tasks:
        print fmt % (i, clean_name(title) + ext, file_id)
        i += 1

def command_ls(the_url):
    contents = _gather_contents(the_url)
    msg = "Listing of: %s" % the_url
    print msg, '\n'+'-'*len(msg)
    _print_tasks(_extract_tasks(MusicHandler(), contents), '.mp3')

def main():
    if len(sys.argv) < 2:
        return usage()

    if len(sys.argv) == 3:
        command = sys.argv[1]
        the_url = sys.argv[2]
    else:
        command = 'dl'
        the_url = sys.argv[1]

    if command == 'dl':
        command_dl(the_url)
    elif command == 'ls':
        command_ls(the_url)
    else:
        print "Error: unknown command %s." % command
        return usage()

def usage():
    print 'Usage: %s [dl|ls/*|find|rdl*/] URL' % sys.argv[0]

if __name__ == '__main__':
    main()
