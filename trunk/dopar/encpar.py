#!/usr/bin/env python

import sys
import os
import threading
from Queue import Queue

NUM_PROC = 2
COMMAND_PATTERN = 'nice lame -h -b 64 "%s"'

# example of multiple occurences of the pattern:
# COMMAND_PATTERN = 'nice lame -q 1 -b 64 "%s"; mv "%s".mp3 "%s"'

class EncThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while not self.queue.empty():
            tgt = self.queue.get()
            # support for multiple occurences in the pattern
            format_tuple = (tgt,) * (len(COMMAND_PATTERN.split("%s"))-1)
            print "Started",tgt
            os.popen(COMMAND_PATTERN % format_tuple)
            print "Finished", tgt

def read_env():
    """Change working mode base on environment variables."""
    global COMMAND_PATTERN, NUM_PROC
    COMMAND_PATTERN = os.getenv('COMMAND_PATTERN', COMMAND_PATTERN)
    NUM_PROC = int(os.getenv('NUM_PROC', NUM_PROC))
    print (COMMAND_PATTERN, NUM_PROC)
    
def process_files(files):
    """Run COMMAND_PATTERN for its arguments using NUM_PROC threads."""
    q = Queue()
    map(q.put, files)

    t = [ EncThread(q) for i in xrange(NUM_PROC) ]

    map(lambda p: p.start(), t)
    map(lambda p: p.join(), t)

if __name__=='__main__':
    read_env()
    process_files(sys.argv[1:])
    
