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


class Remote:
    def __init__(self, name, raw_url=None):
        self.name = name
        self.protocol = None
        self.host = None
        self.path = None
        if raw_url:
            self.parse(raw_url)

    def parse(self, raw_url):
        if raw_url.startswith('git@'):
            self.parse_ssh(raw_url)
        else:
            self.parse_https(raw_url)

    def parse_ssh(self, raw_url):
        self.protocol = 'git@'
        userhost, self.path = raw_url.split(':')
        self.host = userhost.split('@')[1]

    def parse_https(self, raw_url):
        parsed = urlparse(raw_url)
        self.protocol = parsed.scheme + '://'
        self.host = parsed.netloc
        self.path = parsed.path[1:]

    def render_url(self):
        return ''.join([self.protocol, self.host, ':' if self.protocol=='git@' else '/', self.path])



remotes = os.popen("git remote -vv").readlines()
remote = Remote(*remotes[0].split()[:2])

remote.host = next(arg for arg in sys.argv[1:] if not arg.startswith('-'))
echo_exec('git remote set-url {} {}'.format(remote.name, remote.render_url()))

print('Done.')
