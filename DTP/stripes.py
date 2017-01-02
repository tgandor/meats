#!/usr/bin/env python

import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('count', type=int, default=11, nargs='?', help='Number of stripes')
parser.add_argument('--top', type=float, default=0.0, help='Margin top [cm]')
parser.add_argument('--bottom', type=float, default=0.0, help='Margin bottom [cm]')
args = parser.parse_args(sys.argv[1:])

count = args.count
print('Will print {} lines (for {} stripes)'.format(count-1, count))

distance = (A4[1] - args.top*cm - args.bottom*cm) / count
print('Each stripe will be {:.3f} cm wide.'.format(distance / cm))

c = canvas.Canvas('out.pdf')
c.setDash(4, 8)
c.setLineWidth(0.25)

for i in range(1, count):
    y = args.bottom*cm + i*distance
    c.line(0, y, A4[0], y)

c.save()

if sys.platform.startswith('linux'):
    if os.system('lp out.pdf') != 0:
        os.system('xdg-open out.pdf')
else:
    # http://stackoverflow.com/questions/12723818/print-to-standard-printer-from-python
    os.startfile('out.pdf', 'print')
os.unlink('out.pdf')
