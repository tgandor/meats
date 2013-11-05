#!/usr/bin/env python

import os
import sys
import time

def timed(cmd):
    start = time.time()
    os.system(cmd)
    return time.time() - start

def human(x):
    for sufix in ['', 'k', 'M', 'G']:
        if x < 1024:
            return "%.1f %s" % (x, sufix)
        x /= 1024.0
    return "%.1f P" % x

compressors = [
    ('gzip',  'gzip -9 %s', '%s.gz', 'gunzip %s.gz'),
    ('bzip2', 'bzip2 %s', '%s.bz2', 'bunzip2 %s.bz2'),
    ('gzip',  'gzip -9 %s', '%s.gz', 'gunzip %s.gz'),
    ('lzip',  'lzip -9 %s', '%s.lz', 'lzip -d %s.lz'),
    ('plzip',  'plzip -9 %s', '%s.lz', 'plzip -d %s.lz'),
    ('lzma',  'lzma -9 %s', '%s.lzma', 'lzma -d %s.lzma'),
]

for f in sys.argv[1:]:
    origsize = os.path.getsize(f)
    print "Bechmarking file:", f, 'size:', '%sB' % human(origsize), '(%d)' % origsize
    for name, comp, out, decomp in compressors:
        if os.system('which %s > /dev/null' % name) == 0:
            print "  Testing", name
            elap = timed(comp % f)
            compsize = os.path.getsize(out % f)
            print '    Size after: %5sB (%d), %4.1f%% size (factor %5.2f).' % (
                human(compsize), compsize, 100.0*compsize/origsize, float(origsize)/compsize
            )
            print '    Compressed in %5.3f s, in: %8sB/s, out %8sB/s.' % (elap,  human(origsize/elap),  human(compsize/elap))
            elap2 = timed(decomp % f)
            print '    Decompress in %5.3f s, in: %8sB/s, out %8sB/s.' % (elap2, human(compsize/elap2), human(origsize/elap2))
            print '-'*40
