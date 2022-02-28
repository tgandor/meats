#!/usr/bin/env python

"""
Find string in XML (tags, attribute names, attribute values).
"""

import argparse
from xml.etree import ElementTree as ET


def check(value: str, pattern: str, **options):
    if options.get("case_insensitive"):
        return pattern.casefold() in value.casefold()
    return pattern in value


def render(name, **options):
    for key, val in options.get("nsmap", {}).items():
        name = name.replace("{" + val + "}", f"{key}:")
    return name


def search_recursive(node: ET.Element, pattern, path=None, **options):
    if path is None:
        path = []
    path.append(render(node.tag, **options))

    if check(node.tag, pattern, **options):
        print("/".join(path))

    for key, val in node.attrib.items():
        if check(key, pattern, **options) or check(val, pattern, **options):
            print("/".join(path + [f"@{render(key, **options)} = {val}"]))

    for child in node:
        search_recursive(child, pattern, path, **options)

    path.pop()


def gather_nsmap(node):
    nsmap = node.nsmap
    for child in node:
        nsmap |= gather_nsmap(child)
    return nsmap


def load_xml(path: str):
    try:
        from lxml.etree import parse

        tree = parse(path)
        root = tree.getroot()
        nsmap = gather_nsmap(root)
    except ImportError:
        tree = ET.parse(path)
        root = tree.getroot()
        nsmap = {}
    return root, nsmap


parser = argparse.ArgumentParser()
parser.add_argument("pattern")
parser.add_argument("xml_file", nargs="+")
parser.add_argument("--case-insensitive", "-c", action="store_true")
args = parser.parse_args()

for path in args.xml_file:
    print(path)
    root, nsmap = load_xml(path)
    if nsmap:
        print(nsmap)
    search_recursive(
        root, args.pattern, case_insensitive=args.case_insensitive, nsmap=nsmap
    )
