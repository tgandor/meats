#!/usr/bin/env python

import argparse
import re

import pypdf

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("--output", "-o")
parser.add_argument("page_specs", nargs="+")
args = parser.parse_args()


def get_page_numbers(page_specs):
    for spec in page_specs:
        if re.match(r"\d+$", spec):
            yield int(spec) - 1
            continue

        m = re.match(r"(\d+)-(\d+)$", spec)
        if m:
            low = int(m.group(1)) - 1
            high = int(m.group(2))

            for i in range(low, high):
                yield i

            continue


with open(args.input_file, "rb") as input_file:
    input_pdf = pypdf.PdfReader(input_file)
    output = pypdf.PdfWriter()

    for i in get_page_numbers(args.page_specs):
        print(f"Getting page {i+1} ({i=})")
        output.add_page(input_pdf.pages[i])

    output_file = args.output or "part_" + args.input_file
    print("Writing pages to:", output_file)
    with open(output_file, "wb") as outf:
        output.write(outf)
