#!/usr/bin/env python

import os
import re
import sys
import time

class Bulker(object):
    VALUES = ') VALUES '

    def __init__(self, max_packet=2**22, output=sys.stdout):
        self.max_packet = max_packet
        self.out_stream = output
        self.in_bulk = False
        self.current_packet = 0
        self.current_prefix = ''

    def output(self, s):
        """Print s counting len towards current_packet."""
        self.current_packet += len(s)
        self.out_stream.write(s)

    def end_bulk(self):
        if not self.in_bulk:
            return
        self.out_stream.write(';\n')
        self.current_packet = 0
        self.in_bulk = False

    def process_line(self, line):
        # filter away irrelevant lines
        if not line.startswith('INSERT INTO'):
            self.end_bulk()
            self.out_stream.write(line)
            return

        prefix, values = line.split(self.VALUES)
        trimmed_values = values[:values.rfind(';')]
        # sys.stderr.write('Prefix: ' + prefix + '\n')
        # sys.stderr.write('Values: ' + values + '\n')

        # normal or emergency end bulk
        if prefix != self.current_prefix:
            self.end_bulk()

        # buffer overflow end bulk
        if self.current_packet + len(values) + 3 > self.max_packet:
            self.end_bulk()

        # start bulk
        if not self.in_bulk:
            self.current_prefix = prefix
            trimmed = line[:line.rfind(';')]
            self.output(prefix + self.VALUES + '\n ' + trimmed_values)
            self.in_bulk = True
        else:
            # sys.stderr.write('Trimmed Values: ' + trimmed_values + '\n')
            self.output(',\n '+trimmed_values)

    def close(self):
        self.end_bulk()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        in_stream = sys.stdin
    else:
        in_stream = open(sys.argv[1])

    bulker = Bulker()

    for line in in_stream:
        bulker.process_line(line)

    bulker.close()
