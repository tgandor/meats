#!/usr/bin/env python

import os
import sys
from collections import defaultdict


class FileStats:
    def __init__(self):
        self.stats_b = defaultdict(int)
        self.stats_4K = defaultdict(int)
        self.counted_files = set()
        self.total_b = 0
        self.total_4K = 0

    def process_file(self, filepath):
        if filepath in self.counted_files or os.path.islink(filepath):
            return
        self.counted_files.add(filepath)
        ext = os.path.splitext(filepath)[1].lower()
        size = os.stat(filepath).st_size
        blocks = (size + 2**12 - 1) // (2 ** 12)
        self.stats_b[ext] += size
        self.total_b += size
        self.stats_4K[ext] += blocks
        self.total_4K += blocks

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
        for ext, size in self.get_stats_b():
            print('{:4s}: {:16,} B ({:4.1f}%)'.format(ext, size, 100.0 * size / self.total_b))
        print('Total:{:16,} B\n{}'.format(self.total_b, '-'*40))

    def summary_4K(self):
        print('Summary of size in KB, assuming ceil(size/4KB):')
        for ext, blocks in self.get_stats_4K():
            print('{:4s}: {:12,} KB ({:4.1f}%)'.format(ext, blocks * 4, 100.0 * blocks / self.total_4K))
        print('Total:{:12,} KB\n{}'.format(self.total_4K * 4, '-'*40))


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
