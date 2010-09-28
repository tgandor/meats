import sys

que = open(open('pipename').read(), 'w')
for n in sys.argv[1:]:
    print >>que, n
que.close()
