#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
import argparse
import os
import time


def timed(cmd):
    start = time.time()
    os.system(cmd)
    return time.time() - start


def human(x):
    for suffix in ["", "K", "M", "G", "T"]:
        if x < 1024:
            return "%.1f %s" % (x, suffix)
        x /= 1024
    return "%.1f P" % x


try:
    from shutil import which  # type: ignore
except ImportError:

    def which(program):
        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None


known_compressors = [
    ("bzip2", "bzip2 %(f)s", "%s.bz2", "bunzip2 %(f)s.bz2"),
    ("gzip", "gzip -9 %(f)s", "%s.gz", "gunzip %(f)s.gz"),
    ("lzip", "lzip -9 %(f)s", "%s.lz", "lzip -d %(f)s.lz"),
    ("lzma", "lzma -9 %(f)s", "%s.lzma", "lzma -d %(f)s.lzma"),
    ("lzop", "lzop -3 %(f)s", "%s.lzo", "lzop -d -f %(f)s.lzo; rm %(f)s.lzo"),
    ("lzop", "lzop -9 %(f)s", "%s.lzo", "lzop -d -f %(f)s.lzo; rm %(f)s.lzo"),
    ("pigz", "pigz -9 %(f)s", "%s.gz", "pigz -d %(f)s.gz"),
    ("plzip", "plzip -0 %(f)s", "%s.lz", "plzip -d %(f)s.lz"),
    ("plzip", "plzip -6 %(f)s", "%s.lz", "plzip -d %(f)s.lz"),
    ("plzip", "plzip -9 %(f)s", "%s.lz", "plzip -d %(f)s.lz"),
    ("xz", "xz -9 %(f)s", "%s.xz", "xz -d %(f)s.xz"),
    (
        "zip",
        "zip -q -9 %(f)s.zip %(f)s",
        "%s.zip",
        "unzip -q -o %(f)s.zip; rm %(f)s.zip",
    ),
    ("zstd", "zstd -q %(f)s; rm %(f)s", "%s.zst", "unzstd -q %(f)s.zst; rm %(f)s.zst"),
]

FAST = {
    "pigz -9 %(f)s",
    "lzop -3 %(f)s",
    "zstd",
    "plzip -0 %(f)s",
    "plzip -6 %(f)s",  # quite slow, but acceptable
    "zstd -q %(f)s; rm %(f)s",
}
parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+")
parser.add_argument("--all", "-a", action="store_true", help="include slow / redundant")
args = parser.parse_args()

compressors = []
for comp in known_compressors:
    if not which(comp[0]):
        print("Skipping %s (program not found)" % comp[0])
        continue

    if comp[1] not in FAST and not args.all:
        print("... skipping %s (use --all to include in tests)" % comp[1])
    else:
        compressors.append(comp)
print()

for f in args.files:
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
            print("  Testing", name, ":", comp % dict(f=f), "...")
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
