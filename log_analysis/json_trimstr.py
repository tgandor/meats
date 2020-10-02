#!/usr/bin/env python

from json.decoder import scanstring
from functools import singledispatch
import argparse
import json

LIMIT = 120
SAMPLE = 80

parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()


def trim_scanstring(*args, **kwargs):
    """This never gets called."""
    print('TRIMMING SCANSTR')
    s, end = scanstring(*args, **kwargs)
    print('end', end)
    if len(s) > LIMIT:
        s = s[:SAMPLE] + '...'
    return s, end


class TrimmingDecoder(json.JSONDecoder):
    """This doesn't work."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parse_string = trim_scanstring


@singledispatch
def trim(item):
    return item


@trim.register(list)
def trim_list(item):
    return [trim(subitem) for subitem in item]


@trim.register(dict)
def trim_dict(item):
    return {key: trim(value) for key, value in item.items()}


@trim.register(str)
def trim_str(item):
    return item if len(item) <= LIMIT else item[:SAMPLE] + '(...)'


with open(args.file) as f:
    data = json.load(f, cls=TrimmingDecoder)
    data = trim(data)
    print(json.dumps(data, indent=2))
