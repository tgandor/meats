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
parser.add_argument('--bare', '-b', action='store_true', help='all hrefs (no link text)')
parser.add_argument('--text', '-t', action='store_true', help='Display link text')
parser.add_argument('--nested', '-n', action='store_true', help='Match anchor tags which can include nested tags')
args = parser.parse_args()

url_or_path = args.url_or_path

if os.path.isfile(url_or_path):
    data = open(url_or_path).read()
else:
    data = requests.get(url_or_path).text

if args.nested:
    # match link text via non greedy .+
    link = re.compile(r'<a (?:\w+="[^"]+" )*href="(?P<href>[^"]+)"(?: \w+="[^"]+")*>(?P<text>.+?)</a>', re.IGNORECASE)
elif args.bare:
    link = re.compile(r'href=["\'](?P<href>[^"\']+)["\']', re.IGNORECASE)
else:
    link = re.compile(r'href="(?P<href>[^"]+)"(?: \w+="[^"]+")*>(?P<text>.+?)</a>', re.IGNORECASE)

# tag and closing tag near match
tag = re.compile(r'<[^>]+?>')

for match in link.finditer(data):
    d = match.groupdict()
    if args.text:
        text = d['text']
        if args.nested:
            text, _ = tag.subn('', text)
        print(urllib_parse.urljoin(url_or_path, d['href']), text)
    elif args.bare:
        print(d['href'])
    else:
        print(urllib_parse.urljoin(url_or_path, d['href']))
