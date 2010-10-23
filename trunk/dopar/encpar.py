#!/usr/bin/env python

import sys
import os
import threading
from Queue import Queue

NUM_PROC = 2
COMMAND_PATTERN = 'nice lame -h -b 64 "%s"'

class EncThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while not self.queue.empty():
            tgt = self.queue.get()
            print "Started",tgt
            os.popen(COMMAND_PATTERN % tgt)
            print "Finished",tgt

def process_files(files):
    """Run COMMAND_PATTERN for its arguments using NUM_PROC threads."""
    q = Queue()
    map(q.put, files)

    t = [ EncThread(q) for i in xrange(NUM_PROC) ]

    map(lambda p: p.start(), t)
    map(lambda p: p.join(), t)

if __name__=='__main__':
    process_files(sys.argv[1:])
    
