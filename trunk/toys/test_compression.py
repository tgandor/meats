#!/usr/bin/env python

import os
import sys
import time

def timed(cmd):
    start = time.time()
    os.system(cmd)
    return time.time() - start

def human(x):
    for sufix in ['', 'K', 'M', 'G', 'T']:
        if x < 1024:
            return "%.1f %s" % (x, sufix)
        x /= 1024.0
    return "%.1f P" % x

compressors = [
    ('bzip2', 'bzip2 %(f)s'               , '%s.bz2'  , 'bunzip2 %(f)s.bz2'                   ),
    ('gzip',  'gzip -9 %(f)s'             , '%s.gz'   , 'gunzip %(f)s.gz'                     ),
    ('lzip',  'lzip -9 %(f)s'             , '%s.lz'   , 'lzip -d %(f)s.lz'                    ),
    ('plzip', 'plzip -9 %(f)s'            , '%s.lz'   , 'plzip -d %(f)s.lz'                   ),
    ('lzma',  'lzma -9 %(f)s'             , '%s.lzma' , 'lzma -d %(f)s.lzma'                  ),
    ('zip',   'zip -q -9 %(f)s.zip %(f)s' , '%s.zip'  , 'unzip -q -o %(f)s.zip; rm %(f)s.zip' ),
]

for f in sys.argv[1:]:
    if not os.path.exists(f):
        print "Skipping %s: file does not exist" % f
        continue
    origsize = os.path.getsize(f)
    if origsize == 0:
        print "Skipping %s: empty file" % f
        continue
    print "Bechmarking file:", f, 'size:', '%sB' % human(origsize), '(%d)' % origsize
    for name, comp, out, decomp in compressors:
        if os.system('which %s > /dev/null' % name) == 0:
            print "  Testing", name
            elap = timed(comp % dict(f=f))
            compsize = os.path.getsize(out % f)
            print '    Size after: %5sB (%d), %4.1f%% size (factor %5.2f).' % (
                human(compsize), compsize, 100.0*compsize/origsize, float(origsize)/compsize
            )
            print '    Compressed in %5.3f s, in: %8sB/s, out %8sB/s.' % (elap,  human(origsize/elap),  human(compsize/elap))
            elap2 = timed(decomp % dict(f=f))
            print '    Decompress in %5.3f s, in: %8sB/s, out %8sB/s.' % (elap2, human(compsize/elap2), human(origsize/elap2))
            print '  ' + '-'*40
    print '=' * 60
