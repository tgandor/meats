#!/usr/bin/env python
import sys

if len(sys.argv) != 2:
    print "Usage:"
    print "  %s SECONDS" % sys.argv[0]
    print "  %s H:M:S" % sys.argv[0]
    exit()

hms = sys.argv[1].split(':')
secs = int(hms[0])
for limb in hms[1:]:
    secs *= 60
    secs += int(limb)
h, s = divmod(secs, 3600)
m, s = divmod(s, 60)
print "%d seconds - %02d:%02d:%02d" % (secs, h, m, s)

