#!/usr/bin/env python

import os
import re
import sys

issue_key = sys.argv[1]

data = sys.stdin.read()

issues = re.findall(f'{re.escape(issue_key)}-\\d+', data)
print('-' * 79)
print(issues)
print('-' * 79)
print(' or '.join(f'key = {key}' for key in issues))

