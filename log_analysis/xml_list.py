#!/usr/bin/env python

"""
List XML elements, with indentation, no closing tags.
For structure it may be nice to use in conjuction with shell filters,
e.g., for counting repeated nested elements, and then unique lines:

    $ python xml_list.py some_file.xml  | uniq -c | nl
"""

import argparse
from xml.etree import ElementTree as ET


def render(element, options):
    result = "<" + element.tag
    if options.get("attribute", False):
        for name in options['attribute']:
            if name in element.attrib:
                result += f" {name}={element.attrib[name]}"
    result += ">"
    return result


def list(element, level=0, options=None):
    if options is None:
        options = {}

    print(". " * level, render(element, options), sep="")

    if level == options.get("max_level", -1):
        return

    for child in element:
        list(child, level + 1, options)


parser = argparse.ArgumentParser()
parser.add_argument("xml_file")
parser.add_argument("--attribute", "-a", nargs="*")
parser.add_argument("--max-level", "-d", type=int, default=-1)
args = parser.parse_args()

tree = ET.parse(args.xml_file)
root = tree.getroot()
list(root, options=vars(args))
