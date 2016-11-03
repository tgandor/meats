#!/usr/bin/env python

import os
import sys
from collections import defaultdict


class FileStats:
    def __init__(self):
        self.stats_b = defaultdict(int)
        self.stats_4K = defaultdict(int)
        self.counted_files = set()

    def process_file(self, filepath):
        if filepath in self.counted_files or os.path.islink(filepath):
            return
        self.counted_files.add(filepath)
        ext = os.path.splitext(filepath)[1].lower()
        size = os.stat(filepath).st_size
        blocks = (size + 2**12 - 1) // (2 ** 12)
        self.stats_b[ext] += size
        self.stats_b['Total'] += size
        self.stats_4K[ext] += blocks
        self.stats_4K['Total'] += blocks

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
        print('Summary of size in bytes:')
        max_ext = max(len(x) for x in self.stats_b.keys()) + 1
        total_b = max(self.stats_b.values())
        max_size = len('{:,}'.format(total_b))
        for ext, size in self.get_stats_b():
            print('{:{}s} {:{},} B ({:3.1f}%)'.format(
                ext + ':', max_ext, size, max_size, 100.0 * size / total_b))

    def summary_4K(self):
        print('Summary of size in KB, assuming ceil(size/4KB):')
        max_ext = max(len(x) for x in self.stats_4K.keys()) + 1
        total_4K = max(self.stats_4K.values())
        max_blocks = len('{:,}'.format(total_4K * 4))
        for ext, blocks in self.get_stats_4K():
            print('{:{}s} {:{},} KB ({:3.1f}%)'.format(
                ext + ':', max_ext, blocks * 4, max_blocks, 100.0 * blocks / total_4K))


def main():
    paths = sys.argv[1:]

    if not paths:
        paths.append('.')

    file_stats = FileStats()

    for path in paths:
        file_stats.process(path)

    file_stats.summary_b()
    file_stats.summary_4K()


if __name__ == '__main__':
    main()
