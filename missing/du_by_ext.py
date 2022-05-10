#!/usr/bin/env python

import argparse
import os
import sys
from collections import defaultdict, Counter

TOTAL = "Total"  # magic summary key


class FileStats:
    def __init__(self, multi=False):
        self.multi = multi
        self.stats_b = defaultdict(int)
        self.stats_4K = defaultdict(int)
        self.extension_counter = Counter()
        self.counted_files = set()

    def _get_ext(self, filepath):
        if not self.multi:
            return os.path.splitext(filepath)[1].lower()
        filepath = os.path.basename(filepath)
        chunks = filepath.split(".")
        if chunks[0] == '':
            # hidden file is not an extension
            chunks.pop(0)
        if len(chunks) <= 1:
            # no extension(s)
            return ''
        return "." + ".".join(chunks[1:])

    def process_file(self, filepath):
        if filepath in self.counted_files or os.path.islink(filepath):
            return
        self.counted_files.add(filepath)
        ext = self._get_ext(filepath)
        size = os.stat(filepath).st_size
        blocks = (size + 2 ** 12 - 1) // (2 ** 12)
        self.stats_b[ext] += size
        self.stats_b[TOTAL] += size
        self.extension_counter[ext] += 1
        self.extension_counter[TOTAL] += 1
        self.stats_4K[ext] += blocks
        self.stats_4K[TOTAL] += blocks

    def process_dir(self, directory):
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                self.process_file(os.path.join(dirpath, filename))

    def process(self, path):
        if os.path.isdir(path):
            self.process_dir(path)
        else:
            self.process_file(path)

    def get_stats_b(self):
        return sorted(self.stats_b.items(), key=lambda x: -x[1])

    def get_stats_4K(self):
        return sorted(self.stats_4K.items(), key=lambda x: -x[1])

    def summary_b(self):
        print("Summary of size in bytes:")
        max_ext = max(len(x) for x in self.stats_b.keys()) + 1
        total_b = max(self.stats_b.values())
        max_size = len("{:,}".format(total_b))
        max_count = len("{:,}".format(max(self.extension_counter.values())))
        for ext, size in self.get_stats_b():
            print(
                "{:{}s} {:{},} B ({:5.1f}%), count: {:{},}, average {:,} B".format(
                    ext + ":",
                    max_ext,
                    size,
                    max_size,
                    100.0 * size / total_b,
                    self.extension_counter[ext],
                    max_count,
                    size // self.extension_counter[ext],
                )
            )

    def summary_4K(self):
        print("Summary of size in KB, assuming ceil(size/4KB):")
        max_ext = max(len(x) for x in self.stats_4K.keys()) + 1
        total_4K = max(self.stats_4K.values())
        max_blocks = len("{:,}".format(total_4K * 4))
        for ext, blocks in self.get_stats_4K():
            print(
                "{:{}s} {:{},} KB ({:3.1f}%)".format(
                    ext + ":",
                    max_ext,
                    blocks * 4,
                    max_blocks,
                    100.0 * blocks / total_4K,
                )
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--multi", "-m", action="store_true", help="handle multiple, like .tar.gz"
    )
    parser.add_argument("paths", nargs="*", default=["."])
    args = parser.parse_args()

    file_stats = FileStats(args.multi)

    for path in args.paths:
        file_stats.process(path)

    file_stats.summary_b()
    # file_stats.summary_4K()


if __name__ == "__main__":
    main()
