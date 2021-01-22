#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import time


def timed(cmd):
    start = time.time()
    os.system(cmd)
    return time.time() - start


def human(x):
    for suffix in ["", "K", "M", "G", "T"]:
        if x < 1024:
            return "%.1f %s" % (x, suffix)
        x /= 1024.0
    return "%.1f P" % x


compressors = [
    ("bzip2", "bzip2 %(f)s", "%s.bz2", "bunzip2 %(f)s.bz2"),
    ("gzip", "gzip -9 %(f)s", "%s.gz", "gunzip %(f)s.gz"),
    ("lzip", "lzip -9 %(f)s", "%s.lz", "lzip -d %(f)s.lz"),
    ("xz", "xz -9 %(f)s", "%s.xz", "xz -d %(f)s.xz"),
    ("lzop", "lzop -9 %(f)s", "%s.lzo", "lzop -d -f %(f)s.lzo"),
    ("plzip", "plzip -9 %(f)s", "%s.lz", "plzip -d %(f)s.lz"),
    ("lzma", "lzma -9 %(f)s", "%s.lzma", "lzma -d %(f)s.lzma"),
    (
        "zip",
        "zip -q -9 %(f)s.zip %(f)s",
        "%s.zip",
        "unzip -q -o %(f)s.zip; rm %(f)s.zip",
    ),
]

for f in sys.argv[1:]:
    if not os.path.exists(f):
        print("Skipping %s: file does not exist" % f)
        continue
    original_size = os.path.getsize(f)
    if original_size == 0:
        print("Skipping %s: empty file" % f)
        continue
    print(
        "Benchmarking file:",
        f,
        "size:",
        "%sB" % human(original_size),
        "(%d)" % original_size,
    )
    for name, comp, out, decompress in compressors:
        if os.system("which %s > /dev/null" % name) == 0:
            print("  Testing", name)
            elapsed = timed(comp % dict(f=f))
            compressed = os.path.getsize(out % f)
            print(
                "    Size after: %5sB (%d), %4.1f%% size (factor %5.2f)."
                % (
                    human(compressed),
                    compressed,
                    100.0 * compressed / original_size,
                    float(original_size) / compressed,
                )
            )
            print(
                "    Compressed in %5.3f s, in: %8sB/s, out %8sB/s."
                % (elapsed, human(original_size / elapsed), human(compressed / elapsed))
            )
            elapsed_2 = timed(decompress % dict(f=f))
            print(
                "    Decompress in %5.3f s, in: %8sB/s, out %8sB/s."
                % (
                    elapsed_2,
                    human(compressed / elapsed_2),
                    human(original_size / elapsed_2),
                )
            )
            print("  " + "-" * 40)
    print("=" * 60)
