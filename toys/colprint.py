#!/usr/bin/env python

import sys

def terminal_size():
    import fcntl, termios, struct
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h

def terminal_width():
    return terminal_size()[1]

class PerCol(object):
    def __init__(self, capacity, sep_width=2):
        self.sep_width = sep_width
        self.capacity = capacity
        self.curr_max = 0
        self.curr_cnt = 0
        self.old_width = 0
        self.colsizes = []
    def current_width(self):
        if self.curr_cnt > 0:
            return self.old_width + self.sep_width + self.curr_max
        return self.old_width
    def eat(self, s):
        len_ = len(s)
        if len_ > self.curr_max:
            self.curr_max = len_
        self.curr_cnt += 1
        if self.curr_cnt == self.capacity:
            self.old_width += self.curr_max + self.sep_width
            self.colsizes.append(self.curr_max)
            self.curr_max = 0
            self.curr_cnt = 0
    def render(self, lines, align=str.ljust):
        len_lines = len(lines)
        for i in xrange(self.capacity):
            line = []
            j = i
            for w in self.colsizes:
                line.append(align(lines[j], w))
                j += self.capacity
            if j < len_lines:
                line.append(align(lines[j], self.curr_max))
            if len(line) > 0:
                print (' '*self.sep_width).join(line)

def try_fit(capacity, lines, width):
    cols = PerCol(capacity)
    for line in lines:
        cols.eat(line)
        if cols.current_width() > width:
            return None
    return cols

if __name__ == '__main__':
    lines = map(str.strip, sys.stdin.readlines())
    width = 80
    options = {}
    if len(sys.argv) > 1:
        try:
            width = int(sys.argv[1])
            if width == 0:
                print "Too narrow"
                exit()
            if width < 0:
                width = -width
                options['align'] = str.rjust
        except:
            print "Error parsing width."
    else:
        try:
            width = terminal_width()
        except:
            print "Error reading terminal width."
    print "Fitting to width: %d..." % width
    i = 1
    while True:
        cols = try_fit(i, lines, width)
        if cols:
            break
        i += 1
    cols.render(lines, **options)

