#!/usr/bin/env python

# OK, the target platform has no 'env'...

from __future__ import absolute_import
from __future__ import print_function

import os
import re
import socket
import sys
import time

import six.moves.urllib.error
import six.moves.urllib.parse
import six.moves.urllib.parse
import six.moves.urllib.request


def human(x):
    for sufix in ['', 'K', 'M', 'G', 'T']:
        if x < 1024:
            return "%.1f %s" % (x, sufix)
        x /= 1024.0
    return "%.1f P" % x


def get(url):
    """Stubborn retrieve data."""
    while True:
        try:
            return six.moves.urllib.request.urlopen(url).read()
        except socket.timeout:
            print("Timed out. Retrying.")
        except socket.error as e:
            print("Other socket error:", e)
            print("Retry in 5 seconds...")
            time.sleep(5)


def down(url):
    f = six.moves.urllib.parse.unquote(os.path.basename(url))
    if os.path.exists(f):
        print("skipped", f)
        return 0
    print("getting", f)
    start = time.time()
    data = get(url)
    size = len(data)
    elapsed = time.time() - start
    print("got %sB in %.1f s (%sB/s), saving" % (human(size), elapsed, human(size / elapsed)))
    open(f, 'wb').write(data)
    return size


def folder_name(url):
    candidate = six.moves.urllib.parse.urlsplit(url).path.split('/')[-2]
    if not candidate:
        print('Could not find folder name, returning generic.')
        return 'new_folder'
    return candidate


def enter_folder(name):
    print("Trying to create '{0}', being in {1}...".format(name, os.getcwd()))
    if not os.path.exists(name):
        os.mkdir(name)
        new_name = name
    elif not os.path.isdir(name):
        print("Error: %s exists, but is not a directory")
        suffix = 1
        new_name = "%s_%d" % (name, suffix)
        while os.path.exists(new_name) and not os.path.isdir(new_name):
            suffix += 1
            new_name = "%s_%d" % (name, suffix)
        os.mkdir(new_name)
    else:
        new_name = name
    os.chdir(new_name)


def download_all(url, search='mp3$'):
    total = 0
    try:
        content = get(url).decode()
        links = sorted(set([link
                            for link in re.findall('href="([^"]+)"', content)
                            if re.search(search, link)]))
        links = [six.moves.urllib.parse.urljoin(url, link)
                 if not link.startswith('http')
                 else link for link in links]
    except Exception as e:
        print("Error retrieving file list:", e)
        return
    print("Found:", links)
    if not links:
        print("No URLs found to follow.")
        # print content
        return
    try:
        enter_folder(folder_name(url))
        for link in links:
            total += down(link)
    finally:
        print("Total downloaded: %sB" % human(total))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        download_all(sys.argv[1])
    elif len(sys.argv) == 3:
        download_all(sys.argv[1], sys.argv[2])
    else:
        print("trying to retrieve from clipboard")
        try:
            import androidhelper
        except ImportError:
            print("Error: couldn't find androidhelper")
            exit()

        URL = androidhelper.Android().getClipboard().result
        download_all(URL)
