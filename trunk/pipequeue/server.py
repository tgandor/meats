#!/usr/bin/env python

import os
import tempfile
import time

operation = 'youtube-dl '

pipe = 'quepipe' # tempfile.mktemp()
if not os.path.exists(pipe):
    os.mkfifo(pipe)

# open('pipename', 'w').write(pipe)

print "> Listening on pipe:", pipe

try:
    que = open(pipe, 'r')
    print "> Pipe opened! (something connected)"
    while True:
        file = que.readline()
        if not file:
            print "Queue empty"
            break
        else:
            print file
            os.system(operation + file)
finally:
    os.remove(pipe)
    # os.remove('pipename')
