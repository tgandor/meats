#!/usr/bin/env python

import os
import sys

if len(sys.argv) < 2:
    sys.stderr.write('Usage: {0} URL\n'.format(sys.argv[0]))
    exit(1)

if os.system('which svn'):
    sys.stderr.write('Subversion client missing. Trying to install...\n')
    os.system('sudo apt-get install subversion')
    if os.system('which svn'):
        sys.stderr.write('Subversion client still not found.\n')
        exit(1)

url_parts = sys.argv[1].split('/')

if url_parts[-1] == '':
    url_parts.pop()

folder_name = ''

if url_parts[-1] == 'trunk':
    folder_name = url_parts[-2]

if url_parts[-2] == 'branches':
    folder_name = '{0}_{1}'.format(url_parts[-3], url_parts[-1])

command = 'time svn co {0} {1}'.format(sys.argv[1], folder_name)
sys.stderr.write('{0}\n'.format(command))
os.system(command)
