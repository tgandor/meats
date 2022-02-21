#!/usr/bin/env python

"""
List XML elements, with indentation, no closing tags.
For structure it may be nice to use in conjuction with shell filters,
e.g., for counting repeated nested elements, and then unique lines:

    $ python xml_list.py some_file.xml  | uniq -c | nl
"""

import argparse
from xml.etree import ElementTree as ET


def list(element, level=0):
    print(". " * level, "<" + element.tag + ">")
    # import code; code.interact(local=locals())
    for child in element:
        list(child, level + 1)


parser = argparse.ArgumentParser()
parser.add_argument("xml_file")
args = parser.parse_args()

tree = ET.parse(args.xml_file)
root = tree.getroot()
list(root)
