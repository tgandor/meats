#!/usr/bin/env python

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import os
import sys


count = int(sys.argv[1]) if (len(sys.argv) > 1) else 11
print('Will print {} lines (for {} stripes)'.format(count-1, count))

distance = A4[1] / count
print('Each stripe will be {:.3f} cm wide.'.format(distance / cm))

c = canvas.Canvas('out.pdf')
c.setDash(4, 8)
c.setLineWidth(0.25)

for i in range(1, count):
    c.line(0, i*distance, A4[0], i*distance)

c.save()

if sys.platform.startswith('linux'):
    if os.system('lp out.pdf') != 0:
        os.system('xdg-open out.pdf')
else:
    # http://stackoverflow.com/questions/12723818/print-to-standard-printer-from-python
    os.startfile('out.pdf', 'print')
os.unlink('out.pdf')
