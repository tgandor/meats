#!/usr/bin/env python

import os


def make_commit_url(repo_url, commit_hash):
    return '{}/commit/{}'.format(repo_url, commit_hash)
    
    
def repo_name(repo_url):
    return repo_url.split('/')[-1]
    
   
last_commit = os.popen("git log -1").readlines()
remote = os.popen("git remote -vv").readlines()

# print last_commit, remote

commit_hash = last_commit[0].split()[1]
repo_url = remote[0].split()[1]
description = ''.join(last_commit[4:])

print("[{} @ {}|{}] {}".format(
    commit_hash[:10], 
    repo_name(repo_url), 
    make_commit_url(repo_url, commit_hash),
    description
))
