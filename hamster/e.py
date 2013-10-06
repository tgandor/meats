
import sys, urllib, os, re, time

def human(x):
    for sufix in ['', 'k', 'M', 'G']:
        if x < 1024:
            return "%.1f %s" % (x, sufix)
        x /= 1024
    return "%.1f P" % x

def get(URL):
  return urllib.urlopen(URL).read()

def down(URL):
  f = os.path.basename(URL)
  if os.path.exists(f):
      print  "skipped", f
      return
  print "getting", f
  start = time.time()
  data = get(URL)
  size = len(data)
  elap = time.time() - start
  print "got %sB in %.1f s (%sB/s), saving" % (human(size), elap, human(size/elap))
  open(f,"w").write(data)

URL = sys.argv[1]

for link in re.findall("http[^\"]+", get (URL)):
  if re.search(sys.argv[2], link):
    down (link)

