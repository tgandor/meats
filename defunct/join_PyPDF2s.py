#!/usr/bin/env python

# There is this thing in PyPDF2:
# https://github.com/mstamy2/PyPDF2/blob/master/Scripts/pdfcat
# But it isn't added to entry_points in setup.py ...

import argparse

from PyPDF2 import PdfFileMerger

parser = argparse.ArgumentParser()
parser.add_argument("--output", "-o", default="joined.pdf")
parser.add_argument("files", nargs="+")
args = parser.parse_args()

merger = PdfFileMerger()
for file in args.files:
    merger.append(open(file, "rb"))

with open(args.output, "wb") as output:
    merger.write(output)
