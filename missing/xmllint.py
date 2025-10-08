#!/usr/bin/env python

"""This is somewhat obsoleted by `xmllint --format file` but has the advantage of
working without installing anything extra (and possibly in-place)."""

import argparse
import glob
import itertools
from xml.dom import minidom

def format_xml(input_path, output_path=False, indent=2):
    with open(input_path, "r", encoding="utf-8") as f:
        xml_str = f.read()

    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent=" " * indent)

    # Usuwamy puste linie (minidom je dodaje)
    pretty_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip()])

    if output_path is False:
        print(pretty_xml)
        return

    if output_path is None:
        output_path = input_path

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="*", help="files or glob expressions to process")
parser.add_argument(
    "--write-back",
    "--inplace",
    "-w",
    "-i",
    action="store_true",
    help="overwrite existing files",
)
args = parser.parse_args()


def rglob(expr):
    if "**" in expr:
        return glob.glob(expr, recursive=True)
    return glob.glob(expr)


files = list(itertools.chain.from_iterable(map(rglob, args.files)))

if len(files) >= 1:
    for filename in files:
        output_path = filename if args.write_back else False
        format_xml(filename, output_path=output_path)
else:
    print("No files provided / found.")
