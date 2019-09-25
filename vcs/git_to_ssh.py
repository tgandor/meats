#!/usr/bin/env python

import os
import sys

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def echo_exec(cmd):
    print('CMD> ' + cmd)
    if '-n' not in sys.argv[1:]:
        os.system(cmd)
    else:
        print(' ... (not running)')


remote = os.popen("git remote -vv").readlines()

remote_name, raw_url = remote[0].split()[:2]

if raw_url.startswith('git@'):
    print('Already on SSH: {} ({})'.format(raw_url, remote_name))
    exit()

print('From: ' + raw_url)
parsed = urlparse(raw_url)

new_url = 'git@{}:{}'.format(parsed.netloc, parsed.path[1:])
print('  To: ' + new_url)

echo_exec('git remote set-url {} {}'.format(remote_name, new_url))

print('Done.')
