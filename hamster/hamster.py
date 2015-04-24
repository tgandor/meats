#!/usr/bin/env python

import sys
import os
import re
import time
import urllib
import random
import cStringIO

urllib.URLopener.version = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0'

CHUNK = 512 * 1024


def info(s, eol='\n'):
    print(s.encode('utf-8')+eol)


def human(x):
    for suffix in ['', 'K', 'M', 'G', 'T']:
        if x < 1024:
            return "%.1f %s" % (x, suffix)
        x /= 1024.0
    return "%.1f P" % x


def get_content(url, cache=[True]):
    if url.endswith('/'):
        # minor unification
        url = url[:-1]
    if not os.path.exists('.hamster'):
        info('Missing .hamster directory, creating...')
        os.mkdir('.hamster')
    from hashlib import md5
    import gzip
    digest = md5(url).hexdigest()
    url_file = os.path.join('.hamster/', digest+'.url')
    content_file = os.path.join('.hamster', digest+'.data')
    if os.path.exists(url_file):
        saved_url = open(url_file).read()
        if saved_url != url:
            info("You're lucky! Found a md5 collision between:\n%s\nand:\n%s" % (saved_url, url))
        cache[0] = True
        if os.path.exists(content_file):
            return open(content_file).read()
        if os.path.exists(content_file+'.gz'):
            return gzip.open(content_file+'.gz', 'rb').read()
        info('Missing data file for: %s' % url)
    info('  (retrieving from the Web...)')
    if not cache[0]:
        time.sleep(random.random()*1.0)
    content = urllib.urlopen(url).read()
    open(url_file, 'wb').write(url)
    f = gzip.open(content_file+'.gz', 'wb', 9)
    f.write(content)
    f.close()
    cache[0] = False
    return content


def clean_name(dirty):
    def parse_uft8(starred):
        starred = starred.group()
        codes = [starred[i:i+2] for i in xrange(1, len(starred), 3)]
        starred = ''.join(chr(int(o, 16)) for o in codes)
        return starred.decode('utf-8')

    dirty = re.sub('(\\*[0-9a-fA-F]{2})+', parse_uft8, dirty)
    dirty = dirty.replace('(', '').replace(')', '')
    return dirty.replace('+', '_')


def read_with_progress(resp):
    start = time.time()
    sio = cStringIO.StringIO()
    for chunk in iter(lambda: resp.read(CHUNK), ''):
        sio.write(chunk)
        sys.stdout.write('.')
        sys.stdout.flush()
    elapsed = time.time() - start
    info(" done: %sB in %.1f s, %sB/s" % (
        human(sio.tell()),
        elapsed,
        human(sio.tell()/elapsed)
    ))
    return sio.getvalue()


def download_url(url):
    resp = urllib.urlopen(url)
    msg = resp.info()
    length = msg.getheader('Content-Length')
    if length:
        info("Downloading %sB " % human(int(length)), eol='')
    return read_with_progress(resp)


class MusicHandler(object):
    pattern = re.compile('/([^/]+),(\d+)\\.mp3', re.IGNORECASE)
    fileext = '.mp3'

    def get_url(self, hostname, file_id):
        ts = int(time.time() * 1000)
        return "http://%s/Audio.ashx?id=%s&type=2&tp=mp3&ts=%d" % (hostname, file_id, ts)

    def get_data(self, hostname, file_id):
        url = self.get_url(hostname, file_id)
        return download_url(url)


class VideoHandler(object):
    pattern = re.compile('/([^/]+),(\d+)\\.(?:avi|mp4)', re.IGNORECASE)
    fileext = '.flv'

    def get_data(self, hostname, file_id):
        url = "http://%s/Video.ashx?id=%s&type=1&file=video" % (hostname, file_id)
        return download_url(url)


def _extract_tasks(handler, contents):
    return sorted(set(sum((handler.pattern.findall(content) for content in contents), [])))


def retrieve_all(hostname, handler, contents, targetdir):
    info("Starting download loop, exit easily with Ctrl-C while sleeping.")
    tasks = _extract_tasks(handler, contents)
    total = len(tasks)
    i = 0
    for title, file_id in tasks:
        title_c = clean_name(title) + handler.fileext
        filename = os.path.join(targetdir, title_c)
        i += 1
        info("%d/%d" % (i, total), eol='')
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            info(">%s< seems to exist, skipping." % filename)
            continue
        info("Retrieving >%s< (id: %s)" % (title_c, file_id))
        data = handler.get_data(hostname, file_id)
        if data.startswith("The page cannot be displayed"):
            info("Reading failed!")
        else:
            open(filename, 'wb').write(data)
        if i == total:
            break
        info("Sleeping...")
        time.sleep(random.random() * 8 + 2)


def _get_inner_content(the_url):
    content = get_content(the_url)
    pos = content.rfind('folderContentContainer')
    if pos == -1:  # backward compatibility?
        return content
    return content[pos:]


def _gather_contents(the_url):
    host_path = re.match('http://[^/]+(/.*)', the_url).group(1)
    contents = [_get_inner_content(the_url)]
    page = 2
    while True:
        next_page = "%s,%d" % (host_path, page)
        info(next_page)
        unquoted = urllib.unquote(next_page)
        last = contents[-1]
        try:
            if last.find(next_page) == -1 and last.find(unquoted) == -1:
                break
        except:
            break
        info("Extra page: " + next_page)
        contents.append(_get_inner_content("%s,%d" % (the_url, page)))
        page += 1
    return contents


def command_dl(the_url):
    hostname = re.match('http://([^/]+)/', the_url).group(1)
    dir_name = clean_name(the_url[the_url.rfind('/')+1:])
    if not os.path.exists(dir_name):
        info("Creating directory: " + dir_name)
        os.mkdir(dir_name)
    else:
        info("Directory %s seems to already exist." % dir_name)

    retrieve_all(hostname, MusicHandler(), _gather_contents(the_url), dir_name)


def _print_tasks(tasks, ext):
    if len(tasks) == 0:
        info(" (empty)")
        return

    fmt = "%%%dd. %%-%ds (id: %%s)" % (
        len(str(len(tasks))),
        max(len(t[0]) for t in tasks) + len(ext),
    )
    i = 1
    for title, file_id in tasks:
        info(fmt % (i, clean_name(title) + ext, file_id))
        i += 1


def command_ls(the_url):
    contents = _gather_contents(the_url)
    msg = "Listing of: %s" % the_url
    print msg, '\n'+'-'*len(msg)
    _print_tasks(_extract_tasks(MusicHandler(), contents), '.mp3')

interesting = []


def command_rls(the_url, level = 2, verbose=False):
    contents = _get_inner_content(the_url)
    base_dir = re.search('/.*$', the_url.replace('http://', '')).group()
    print ' '*level + "Searching", base_dir
    pos = contents.rfind('FilesList')
    subfolder_content = contents[:pos]
    subdirs = []
    for subf in sorted(set(re.findall('<a href="(/[^"]+)"', subfolder_content))):
        if subf.startswith(base_dir+'/'):
            if verbose:
                print ' '*level + subf
            subdirs.append(subf)
    file_content = contents[pos:]
    if verbose:
        print 'FILES:'
    somefiles = []
    for subf in sorted(set(re.findall('<a href="(/[^"]+)"', file_content))):
        if subf.startswith(base_dir+'/'):
            if verbose:
                print ' '*level + subf
            somefiles.append(subf)

    if len(somefiles) == 0:
        print ' '*level + '(empty)'
    else:
        print ' '*level + somefiles[0] + '...'
    if any(sf.endswith('.mp3') for sf in somefiles):
        interesting.append(the_url)
        print ' '*level + 'there are mp3s here.'
    for subf in subdirs:
        command_rls(the_url + subf.replace(base_dir, ''), level+2, verbose)


def command_play(the_url):
    hostname = re.match('http://([^/]+)/', the_url).group(1)
    contents = _gather_contents(the_url)
    msg = "Playing: %s" % the_url
    print msg, '\n'+'-'*len(msg)
    handler = MusicHandler()
    for track, file_id in _extract_tasks(handler, contents):
        url = handler.get_url(hostname, file_id)
        print track, url
        if os.system("mplayer '%s'" % url) != 0:
            print "Unclean exit. quitting."
            break


def command_rdl(the_url):
    command_rls(the_url)
    for url in interesting:
        command_dl(url)


def command_shell(the_url):
    command_rls(the_url)
    if len(interesting) == 0:
        print "No playable or downloadable files."
        return
    hostname = re.match('http://([^/]+)/', the_url).group(1)
    if len(interesting) > 1:
        print "Choose folder:"
        for i, f in zip(range(len(interesting)), interesting):
            print i, f.replace(hostname, '')
        choice = int(raw_input())
        the_url = interesting[choice]
    contents = _gather_contents(the_url)
    handler = MusicHandler()
    tasks = _extract_tasks(handler, contents)
    while True:
        for i in xrange(len(tasks)):
            print i, tasks[i][0]
        cmd = raw_input()
        if cmd == 'q':
            return
        idx = int(cmd)
        url = handler.get_url(hostname, tasks[idx][1])
        print "Playing %s from %s..." % (tasks[idx][0], url)
        os.system("mplayer '%s'" % url)


def command_find(the_url, query):
    command_rls(the_url)
    for i in interesting:
        if i.lower().find(query.lower()) != -1:
            print i


def main():
    if len(sys.argv) < 2:
        # maybe phone clipboard
        try:
            import androidhelper
            print "trying to retrieve from clipboard"
        except ImportError:
            return usage()

        # go to the right location
        try:
            os.chdir('/mnt/sdcard/Download')
        except OSError:
            pass
        the_url = androidhelper.Android().getClipboard().result
        command = 'dl'
    elif len(sys.argv) == 4:
        command = sys.argv[1]
        the_url = sys.argv[2]
        query = sys.argv[3]
    elif len(sys.argv) == 3:
        command = sys.argv[1]
        the_url = sys.argv[2]
    else:
        command = 'rdl'
        the_url = sys.argv[1]

    if command == 'dl':
        command_dl(the_url)
    elif command == 'ls':
        command_ls(the_url)
    elif command == 'find':
        command_find(the_url, query)
    elif command == 'play':
        command_play(the_url)
    elif command == 'shell':
        command_shell(the_url)
    elif command == 'rdl':
        command_rdl(the_url)
    elif command == 'rls':
        try:
            command_rls(the_url)
        except KeyboardInterrupt:
            pass
        if len(interesting):
            print len(interesting), 'Interesting folders:'
        for ifolder in interesting:
            print ifolder
    else:
        print "Error: unknown command %s." % command
        return usage()


def usage():
    print 'Usage: %s [dl|ls|rls|rdl|play] URL' % sys.argv[0]

if __name__ == '__main__':
    main()
