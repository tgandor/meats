#!/usr/bin/env python

import re
import sys

if len(sys.argv) < 3:
	print 'Usage: %s <w_from>x<h_from> <w_to>x<h_to>' % sys.argv[0]
	exit()

# w_from, h_from = map(int, sys.argv[1].split('x'))
# w_to, h_to = map(int, sys.argv[2].split('x'))

w_from, h_from = map(int, re.split('\D', sys.argv[1]))
w_to, h_to = map(int, re.split('\D', sys.argv[2]))

if any(x <= 0 for x in (w_from, h_from, w_to, h_to)):
	print 'All dimensions must be greater than zero.'
	exit()

if w_from * h_to == w_to * h_from:
	print 'Equal aspect. Scale directly to %dx%d.' % (w_to, h_to)
elif w_from * h_to < w_to * h_from:
	print 'Aspect wider in output (%.2f vs %.2f in input).' % (
		float(w_to)/h_to,
		float(w_from)/h_from
	)
	print 'Max horizontal fit: %dx%d.' % (w_to, h_from * w_to / w_from)
else:
	print 'Aspect narrower in output (%.2f vs %.2f in input).' % (
		float(w_to)/h_to,
		float(w_from)/h_from
	)
	print 'Max vertical fit: %dx%d.' % (w_from * h_to / w_to, h_to)

