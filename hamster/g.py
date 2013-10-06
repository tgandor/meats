
import sys, urllib, os

URL= sys.argv[1]
f=os.path.basename(URL)

print "downloading", f
Data = urllib.urlopen(URL).read ()
print "saving"
open (f,"w").write (Data)
