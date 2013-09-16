#!/usr/bin/env python
import sys

def print_secs(secs):
	h, s = divmod(secs, 3600)
	m, s = divmod(s, 60)
	print "%d seconds - %02d:%02d:%02d" % (secs, h, m, s)

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

print_secs(secs)

if secs > 24 * 3600: 
	days, rest = divmod(secs, 24 * 3600)
	print days, 'days',
	print_secs(rest)
	if days > 7:
		weeks, rdays = divmod(days, 7)
		print weeks, 'weeks', rdays, 'days',
		print_secs(rest)
		if weeks > 52: # rough!
			years, rweeks = divmod(weeks, 52)
			print years, 'years', rweeks, 'weeks', rdays, 'days',
			print_secs(rest)

