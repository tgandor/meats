#!/usr/bin/env python

import argparse
import os

from pypdf import PdfWriter  # PdfMerger is deprecated

parser = argparse.ArgumentParser()
parser.add_argument("--output", "-o", default="joined.pdf")
parser.add_argument("--toc", action="store_true", help="Add table of contents")
parser.add_argument("--title", "-t", help="Title for the PDF document")
parser.add_argument("files", nargs="+")
args = parser.parse_args()

merger = PdfWriter()

for file in args.files:
    if args.toc:
        title = os.path.basename(file)
        title = os.path.splitext(title)[0]  # Remove file extension
        merger.add_outline_item(title=title, page_number=len(merger.pages))
    merger.append(open(file, "rb"))

if args.title:
    merger.add_metadata({"Title": args.title})

with open(args.output, "wb") as output:
    merger.write(output)
