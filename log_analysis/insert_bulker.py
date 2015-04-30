#!/usr/bin/env python

import gzip
import itertools
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


def separate_args(arg_v):
    if '--' in arg_v:
        split = arg_v.index('--')
        post_args = arg_v[split+1:]
        arg_v = arg_v[:split]
    else:
        post_args = []
    options = [option for option in arg_v if option.startswith('-')]
    args = [arg for arg in arg_v if not arg.startswith('-')]
    return args + post_args, options


def open_or_unzip(filename):
    if not os.path.exists(filename):
        sys.stderr.write('Warning: file {0} not found.\n'.format(filename))
        return []
    if filename.endswith('.gz'):
        return gzip.open(filename)
    return open(filename)


if __name__ == '__main__':
    args, options = separate_args(sys.argv[1:])
    if len(args) < 0:
        in_stream = sys.stdin
    else:
        in_stream = itertools.chain.from_iterable(itertools.imap(open_or_unzip, args))

    bulker = Bulker()

    if '--engine' in options:
        for line in in_stream:
            bulker.process_line(line.replace('InnoDB', 'MyISAM'))
    else:
        for line in in_stream:
            bulker.process_line(line)

    bulker.close()
