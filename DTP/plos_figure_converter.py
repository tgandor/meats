#!/usr/bin/env python

import argparse
import os
import pathlib
import re

# import subprocess
import sys


def convert(in_file, out_eps):
    print(f"Converting {in_file} to {out_eps}...", file=sys.stderr)
    # I wanted to give subprocess a chance...
    if in_file.endswith(".pdf"):
        # subprocess.call('pdftops -eps', in_file, out_eps)
        os.system(f"pdftops -eps {in_file} {out_eps}")
    elif in_file.endswith(".png"):
        # subprocess.call('convert -format eps', in_file, out_eps)
        os.system(f"convert -format eps {in_file} {out_eps}")


parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
parser.add_argument(
    "--no-include", "-n", action="store_true", help="no includegraphics in output"
)
parser.add_argument(
    "--no-convert", "-f", action="store_true", help="no mogrify/pdftops to FigN.eps"
)
args = parser.parse_args()
graphics = re.compile(r"\\includegraphics([^{]*)\{([a-zA-Z0-9_/.]+)\}")

fig = 0
with args.input.open() as fs:
    while line := fs.readline():
        # line = line.strip()
        if m := graphics.match(line.strip()):
            fig += 1
            # print(fig, line, m.groups())
            _, graphic = m.groups()
            out_eps = f"Fig{fig}.eps"
            if not args.no_convert:
                convert(graphic, out_eps)
            line = line.replace(graphic, out_eps)
            if args.no_include:
                # commenting out doesn't work?
                # line = '%' + line
                continue
        sys.stdout.write(line)
