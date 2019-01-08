#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import re

from six.moves import urllib_parse

# maybe future alternative for parsing (instead of regex):
# import bs4
import requests

parser = argparse.ArgumentParser()
parser.add_argument('url_or_path')
parser.add_argument('--text', '-t', action='store_true', help='Display link text')
args = parser.parse_args()

url_or_path = args.url_or_path

if os.path.isfile(url_or_path):
    data = open(url_or_path).read()
else:
    data = requests.get(url_or_path).text

link = re.compile(r'<a (?:\w+="[^"]+" )*href="(?P<href>[^"]+)"(?: \w+="[^"]+")*>(?P<text>[^<]+)</a>', re.IGNORECASE)

for match in link.finditer(data):
    d = match.groupdict()

    if args.text:
        print(urllib_parse.urljoin(url_or_path, d['href']), d['text'])
    else:
        print(urllib_parse.urljoin(url_or_path, d['href']))
