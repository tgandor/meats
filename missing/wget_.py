#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import time

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

CHUNK = 1024 * 1024


def human(x):
    for suffix in ['', 'K', 'M', 'G', 'T']:
        if x < 1024:
            return "%.1f %s" % (x, suffix)
        x /= 1024.0
    return "%.1f P" % x


def dot_report(total, elapsed):
    sys.stdout.write('.')
    try:  # QPython, has no flush...
        sys.stdout.flush()
    except AttributeError:
        pass


def download(url, report=dot_report):
    f = os.path.basename(url)
    print("downloading", f)
    start = time.time()
    elapsed = size = 0
    with open(f, "wb") as fp:
        resp = urlopen(url)
        for data in iter(lambda: resp.read(CHUNK), b''):
            fp.write(data)
            size += len(data)
            elapsed = time.time() - start
            report(size, elapsed)
    print("\ngot %sB in %.1f s (%sB/s), saved" % (human(size), elapsed, human(size/elapsed)))


if len(sys.argv) > 1:
    # arguments
    for url in sys.argv[1:]:
        download(url)
    exit()
else:
    # QPython clipboard
    print("trying to retrieve from clipboard")
    try:
        import androidhelper

        try:
            os.chdir(os.path.dirname(__file__) + '/../../Download')
        except OSError:
            pass

        url = androidhelper.Android().getClipboard().result
        download(url)
        exit()

    except ImportError:
        print("Error: couldn't find androidhelper")

print('Reading URLs from standard input')
for url in sys.stdin:
    download(url.strip())
