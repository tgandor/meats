#!/usr/bin/env python

# OK, the target platform has no 'env'...

import sys, urllib, os, time

CHUNK = 1024 * 1024

def human(x):
    for sufix in ['', 'K', 'M', 'G', 'T']:
        if x < 1024:
            return "%.1f %s" % (x, sufix)
        x /= 1024.0
    return "%.1f P" % x

def dot_report(total, elapsed):
    sys.stdout.write('.')
    try: # QPython, has no flush...
        sys.stdout.flush()
    except:
        pass

def download(URL, report = dot_report):
    f = os.path.basename(URL)
    print "downloading", f
    start = time.time()
    size = 0
    with open(f, "w") as fp:
        resp = urllib.urlopen(URL)
        for data in iter(lambda: resp.read(CHUNK), ''):
            fp.write(data)
            size += len(data)
            elap = time.time() - start
            report(size, elap)
    print "\ngot %sB in %.1f s (%sB/s), saved" % (human(size), elap, human(size/elap))

if len(sys.argv) > 1:
    for URL in sys.argv[1:]:
        download(URL)
else:
    print "trying to retrieve from clipboard"
    try:
        import androidhelper
    except:
        print "Error: couldn't find androidhelper"
        exit()
    try:
        os.chdir('/mnt/sdcard/external_sd/')
    except:
        try:
            os.chdir('/mnt/sdcard/')
        except:
            pass
    URL = androidhelper.Android().getClipboard().result
    download(URL)
