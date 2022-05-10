#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+")
args = parser.parse_args()

compressed = 0
total = 0

for f in args.files:
    print(f)
    size = os.stat(f).st_size
    with open(f, "rb") as bf:
        bf.seek(-4, os.SEEK_END)
        last = bf.read(4)
        uncompressed = int.from_bytes(last, "little")
    print(f, size, uncompressed, last)
    total += uncompressed
    compressed += size

print(f"Total uncompressed: {total:,} B, compressed {compressed:,} B. Ratio: {compressed/total:.3f}.")


