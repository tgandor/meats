
import sys, urllib, os, time

def human(x):
    for sufix in ['', 'k', 'M', 'G']:
        if x < 1024:
            return "%.1f %s" % (x, sufix)
        x /= 1024
    return "%.1f P" % x

URL = sys.argv[1]
f = os.path.basename(URL)

start = time.time()
print "downloading", f
data = urllib.urlopen(URL).read()
size = len(data)
elap = time.time() - start
print "got %sB in %.1f s (%sB/s), saving" % (human(size), elap, human(size/elap))
open(f, "w").write(data)
