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


new_server = sys.argv[1]

remote = os.popen("git remote -vv").readlines()

raw_url = remote[0].split()[1]
https_url = raw_url.replace(':', '/').replace('git@', 'https://') if raw_url.startswith('git@') else raw_url
parsed = urlparse(https_url)

print('From: ' + raw_url)
if https_url != raw_url:
    print(' Via: ' + https_url)

new_url = parsed._replace(netloc=new_server)
print('  To: ' + new_url.geturl())

remote_name = remote[0].split()[0]

echo_exec('git remote rm {}'.format(remote_name))
echo_exec('git remote add {} {}'.format(remote_name, new_url.geturl()))
echo_exec('git pull {}'.format(remote_name))

branches = [branch.replace('*', '').strip() for branch in os.popen("git branch").readlines()]

for branch in branches:
    echo_exec('git branch --set-upstream-to={}/{} {}'.format(remote_name, branch, branch))



print('Done.')
