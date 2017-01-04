#!/usr/bin/env python

import argparse
import os
import sys

from clipboard_copy import copy


def make_commit_url(repo_url, commit_hash):
    return '{}/commit/{}'.format(repo_url, commit_hash)


def repo_name(repo_url):
    return repo_url.split('/')[-1]


def make_repo_url(fetch_url):
    if 'git@' in fetch_url:
        fetch_url = fetch_url.replace(':', '/').replace('git@', 'https://')
    return fetch_url[:-4] if fetch_url.endswith('.git') else fetch_url


def extract_commits(count):
    log = os.popen("git log -{}".format(count)).readlines()
    lines = []
    for line in log:
        if line.startswith('commit ') and lines:
            yield lines
            lines = []
        lines.append(line)
    yield lines


parser = argparse.ArgumentParser()
parser.add_argument('count', default=1, type=int, nargs='?', help='number of last commits to process')
args = parser.parse_args(sys.argv[1:])

remote = os.popen("git remote -vv").readlines()
repo_url = make_repo_url(remote[0].split()[1])

messages = []

for last_commit in extract_commits(args.count):
    commit_hash = last_commit[0].split()[1]
    description = ''.join(last_commit[4:])
    message = "[{} @ {}|{}] {}".format(
        commit_hash[:10],
        repo_name(repo_url),
        make_commit_url(repo_url, commit_hash),
        description.lstrip()
    )

    messages.append(message)

message = '\n'.join(messages[::-1])

print(message)
copy(message)
