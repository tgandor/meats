#!/usr/bin/env python

"""
Unpack the argument replacing non-ascii characters in filenames.
Careful about rogue archives with absolute paths etc!
"""

import zipfile
import sys
import os

def sanitize(s):
    """Replace 'bad' characters in string with underscore."""
    return ''.join(map(lambda c: c if 31 < ord(c) < 128 else '_', s))

if __name__=='__main__':
    z = zipfile.ZipFile(sys.argv[1])
    for i in z.infolist():
        name_sanitized = sanitize(i.filename)
        if i.file_size:
            open(name_sanitized, 'w').write(z.read(i))
        else:
            os.mkdir(name_sanitized)

