#!/usr/bin/env python

import argparse
import re

import PyPDF2

parser = argparse.ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('--output', '-o')
parser.add_argument('page_specs', nargs='+')
args = parser.parse_args()

# https://stackoverflow.com/questions/39859835/python-split-pdf-by-pages


def get_page_numbers(page_specs):
    for spec in page_specs:
        if re.match(r'\d+$', spec):
            yield int(spec) - 1
            continue

        m = re.match(r'(\d+)-(\d+)$', spec)
        if m:
            low = int(m.group(1)) - 1
            high = int(m.group(2))

            for i in range(low, high):
                yield i

            continue


with open(args.input_file, 'rb') as input_file:
    input_pdf = PyPDF2.PdfFileReader(input_file)

    output = PyPDF2.PdfFileWriter()

    for i in get_page_numbers(args.page_specs):
        print('Getting page', i)
        output.addPage(input_pdf.getPage(i))

    output_file = args.output or 'part_' + args.input_file
    print('Writing pages to:', output_file)
    with open(output_file, 'wb') as outputStream:
        output.write(outputStream)
