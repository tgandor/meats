#!/usr/bin/env python

# OK, the target platform has no 'env'...

import sys, urllib, os, re, time, socket, errno

def human(x):
    for sufix in ['', 'k', 'M', 'G']:
        if x < 1024:
            return "%.1f %s" % (x, sufix)
        x /= 1024.0
    return "%.1f P" % x

def get(URL):
    """Stubborn retrieve data."""
    while True:
        try:
            return urllib.urlopen(URL).read()
        except socket.timeout:
            print "Timed out. Retrying."
        except socket.error as e:
            print "Other socket error:", e
            print "Retry in 5 seconds..."
            time.sleep(5)

def down(URL):
  f = os.path.basename(URL)
  if os.path.exists(f):
      print  "skipped", f
      return 0
  print "getting", f
  start = time.time()
  data = get(URL)
  size = len(data)
  elap = time.time() - start
  print "got %sB in %.1f s (%sB/s), saving" % (human(size), elap, human(size/elap))
  open(f,"w").write(data)
  return size

URL = sys.argv[1]

total = 0
try:
    for link in re.findall("http[^\"]+", get (URL)):
        if re.search(sys.argv[2], link):
            total += down(link)
finally:
    print "Total downloaded: %sB" % human(total)
