#!/usr/bin/env python

import os
import sys


def make_commit_url(repo_url, commit_hash):
    return '{}/commit/{}'.format(repo_url, commit_hash)


def repo_name(repo_url):
    return repo_url.split('/')[-1]


def make_repo_url(fetch_url):
    return fetch_url[:-4] if fetch_url.endswith('.git') else fetch_url


last_commit = os.popen("git log -1").readlines()
remote = os.popen("git remote -vv").readlines()

# print last_commit, remote

commit_hash = last_commit[0].split()[1]
repo_url = make_repo_url(remote[0].split()[1])
description = ''.join(last_commit[4:])

message = "[{} @ {}|{}] {}".format(
    commit_hash[:10], 
    repo_name(repo_url), 
    make_commit_url(repo_url, commit_hash),
    description.lstrip()
)
print(message)

try:
    if sys.version_info.major == 2:
        import Tkinter as Tk
    else:
        import tkinter as Tk
        raw_input = input
    r = Tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(message)
    print('(copied to clipboard)')
    if sys.platform == 'linux2':
        raw_input('Press ENTER after pasting... ')
    r.destroy()
except ImportError:
    pass
