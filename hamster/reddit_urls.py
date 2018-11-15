#!/usr/bin/env python

import json
import sys

feed = json.load(open(sys.argv[1]))

for child in feed['data']['children']:
    print(child['data']['url'])
