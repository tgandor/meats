#!/usr/bin/env python

"""
Unpack the argument replacing non-ascii characters in filenames.
Careful about rogue archives with absolute paths etc!
"""

import zipfile
import sys
import os
import errno

def sanitize(s):
    """Replace 'bad' characters in string with underscore."""
    return ''.join(map(lambda c: c if 31 < ord(c) < 128 else '_', s))

def mkdir_p(name_sanitized, worry=False):
    try:
        os.makedirs(name_sanitized)
        print(" created directory: %s" % name_sanitized)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            if worry:
                print("  directory was present!")
        else:
            raise
    
if __name__=='__main__':
    z = zipfile.ZipFile(sys.argv[1])
    for i in z.infolist():
        name_sanitized = sanitize(i.filename)
        mkdir_p(os.path.dirname(name_sanitized))
        if os.path.basename(name_sanitized) <> '':
            print("Extracting %s from %s..." % (
                os.path.basename(name_sanitized),
                os.path.dirname(name_sanitized)))
            open(name_sanitized, 'w').write(z.read(i))

