#!/usr/bin/env python

import os

raw_branches = list(os.popen('git branch'))
current = [branch.replace('*', '').strip() for branch in raw_branches if '*' in branch][0]
branches = [branch.strip() for branch in raw_branches if '*' not in branch]

os.system('git pull')

for branch in branches:
    os.system(f'git checkout "{branch}"')
    os.system('git pull')

if branches:
    os.system(f'git checkout "{current}"')

