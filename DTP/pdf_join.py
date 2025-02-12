#!/usr/bin/env python

import argparse

from pypdf import PdfWriter  # PdfMerger is deprecated

parser = argparse.ArgumentParser()
parser.add_argument("--output", "-o", default="joined.pdf")
parser.add_argument("files", nargs="+")
args = parser.parse_args()

merger = PdfWriter()
for file in args.files:
    merger.append(open(file, "rb"))

with open(args.output, "wb") as output:
    merger.write(output)
