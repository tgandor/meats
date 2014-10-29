#!/usr/bin/env python

import fnmatch
import os
import re
import subprocess
import sys

# functions from http://stefaanlippens.net/svnignorescript

def svn_propget_svnignore(path):
    '''fetch the svn:ignore property of given path'''
    p = subprocess.Popen(['svn', 'propget', 'svn:ignore', path], stdout=subprocess.PIPE)
    p.wait()
    data = p.stdout.read().strip()
    return data

def svn_propset_svnignore(path, value):
    '''set the svn:ignore property of the given path'''
    p = subprocess.Popen(['svn', 'propset', 'svn:ignore', value, path])
    p.wait()


non_versioned = re.findall('^\?\s+(.+)', os.popen('svn st').read(), re.MULTILINE)

# print non_versioned

for pattern in sys.argv[1:]:
    matching_nonversioned = filter(lambda item: fnmatch.fnmatch(item, pattern), non_versioned)
    # print pattern, matching_nonversioned
    dirs_to_edit = set(map(os.path.dirname, matching_nonversioned))
    print pattern, dirs_to_edit
    for directory in dirs_to_edit:
        current = svn_propget_svnignore(directory)
        print 'Dir: {0}, current svn:ignore {1}'.format(directory, repr(current))
        new_ignore = (current + '\n' if current else '') + pattern
        svn_propset_svnignore(directory, new_ignore)
        current = svn_propget_svnignore(directory)
        print 'Dir: {0}, new svn:ignore {1}'.format(directory, repr(current))

