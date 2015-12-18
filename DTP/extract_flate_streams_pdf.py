#!/usr/bin/env python

import bz2
import sys
import re
import zlib


def find_after(s, needle, startpos=0):
    idx = s.find(needle, startpos)
    if idx != -1:
        return idx + len(needle)
    return idx

class PdfFlateStreamExaminer(object):
    def __init__(self, filename, limit=-1):
        self.filename = filename
        f = open(filename, 'rb')
        self.data = f.read(limit)
        f.close()
        self.current_pos = 0
        self.start = None
        self.end = None
        self.stream_num = 0
        
    def process(self):
        while self.next_stream_start():
            if not self.next_stream_end():
                print("Error - end of stream not found after:", self.current_pos)
                break
            print('Object from {0} to {1} ({2})'.format(self.start, self.end, self.end-self.start))
            self.process_stream_data(self.data[self.start:self.end])
            print('-'*40)
            self.stream_num += 1
        
    def next_stream_start(self):
        flate_filter_pos = self.data.find('/Filter/FlateDecode', self.current_pos)
        if flate_filter_pos == -1:
            flate_filter_pos = self.data.find('/Filter /FlateDecode', self.current_pos)
        if flate_filter_pos == -1:
           return False
        
        self.start = find_after(self.data, 'stream\r\n', flate_filter_pos)
        self.current_pos = self.start
        return True

    def next_stream_end(self):
        self.end = self.data.find('\r\nendstream\r\n', self.current_pos)
        if self.end == -1:
            return False
        self.current_pos = self.end
        return True
        
    def process_stream_data(self, zipped):
        result = zlib.decompress(zipped)
        re_zlib = zlib.compress(result)
        re_bz2 = bz2.compress(result)
        print('Decompressed: %d bytes' % len(result))
        print('Re-deflated: %d bytes' % len(re_zlib))
        print('Re-bzipped2: %d bytes' % len(re_bz2))
        
        output_file = '{0}_stream_{1}.txt'.format(self.filename, self.stream_num)
        open(output_file, 'wb').write(result)
        print('Data saved to: {0}'.format(output_file))
        

if __name__=='__main__':
    PdfFlateStreamExaminer(sys.argv[1]).process()
