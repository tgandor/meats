
import sys, urllib, os, re

URL= sys.argv[1]

def get (URL):
  return urllib.urlopen(URL).read ()

def down(URL):
  f=os.path.basename(URL)
  print "downloading", f
  Data = get (URL)
  print "saving"
  open (f,"w").write (Data)

for link in re.findall("http[^\"]+", get (URL)):
  if re.search (sys.argv [2], link):
    down (link)

# http://www.archive.org/download/tale_of_two_cities_1012_librivox/taleoftwocities_01_dickens_64kb.mp3
