#!/usr/bin/env python

import os
import re
import sys
import time

class Splitter(object):
    def __init__(self, out_dir='.'):
        self.out_dir = out_dir
        self.out_stream = None
        self.table_counter = 0

    def process_line(self, line):
        if line.startswith('DROP TABLE IF EXISTS'):
            self.next_table(line)
        self.output(line)

    def next_table(self, line):
        self.close()
        self.table_counter += 1
        table_name = re.search('DROP TABLE IF EXISTS `?(\w+)`', line).group(1)
        outfile = "{0:02d}_{1}.sql".format(self.table_counter, table_name)
        print('Creating: {0}'.format(outfile))
        self.out_stream = open(os.path.join(self.out_dir, outfile), 'w')

    def output(self, line):
        if self.out_stream:
            self.out_stream.write(line)

    def close(self):
        if self.out_stream:
            self.out_stream.close()
            self.out_stream = None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        in_stream = sys.stdin
    else:
        in_stream = open(sys.argv[1])

    splitter = Splitter()

    for line in in_stream:
        splitter.process_line(line)

    splitter.close()
