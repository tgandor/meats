#!/usr/bin/env python

from __future__ import division
from __future__ import print_function

import re
import sys

if len(sys.argv) < 3:
	print('Usage: %s <w_from>x<h_from> <w_to>x<h_to>' % sys.argv[0])
	exit()

w_from, h_from = list(map(int, re.split('\D', sys.argv[1])))
w_to, h_to = list(map(int, re.split('\D', sys.argv[2])))

if any(x <= 0 for x in (w_from, h_from, w_to, h_to)):
	print('All dimensions must be greater than zero.')
	exit()

if w_from * h_to == w_to * h_from:
	print('Equal aspect. Scale directly to %dx%d Scale: %.3f' % (w_to, h_to, h_to / h_from))
elif w_from * h_to < w_to * h_from:
	print('Aspect wider in output (%.3f vs %.3f in input).' % (
            w_to/h_to, w_from/h_from))
	print('Max horizontal fit: %dx%d Scale: %.3f' % (w_to, int(h_from * w_to / w_from), w_to / w_from))
else:
	print('Aspect narrower in output (%.3f vs %.3f in input).' % (w_to/h_to, w_from/h_from))
	print('Max vertical fit: %dx%d Scale %.3f' % (int(w_from * h_to / w_to), h_to, h_to / h_from))

