#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import re
import sys

"""
A script to replace link targets with their basename - i.e. make it point to local files.
"""

parser = argparse.ArgumentParser()
parser.add_argument('url_or_path')
parser.add_argument('--suffix', help='Ensure a suffix for the links, eg.: .pdf')
args = parser.parse_args()

link = re.compile(r'<a (?:\w+="[^"]+" )*href="(?P<href>[^"]+)"(?: \w+="[^"]+")*>(?P<text>.+?)</a>', re.IGNORECASE)
url_or_path = args.url_or_path

if os.path.isfile(url_or_path):
    data = open(url_or_path).read()
else:
    import requests
    data = requests.get(url_or_path).text


def callback(match):
    if args.suffix and not match.group(1).endswith(args.suffix):
        return match.group().replace(match.group(1), os.path.basename(match.group(1)) + args.suffix)
    return match.group().replace(match.group(1), os.path.basename(match.group(1)))

sys.stdout.write(link.sub(callback, data))
