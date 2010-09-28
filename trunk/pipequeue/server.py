import os
import tempfile
import time

operation = "./youtube-dl -t "
try:
    pipe = tempfile.mktemp()
    os.mkfifo(pipe)
    open('pipename', 'w').write(pipe)
    que = open(pipe, 'r')
    while True:
        file = que.readline()
	if not file:
	    print "Queue empty"
            time.sleep(5)
	else:
            print file
	    os.system(operation + file)
finally:
    que.close()
    os.remove(pipe)
    os.remove('pipename')
    
