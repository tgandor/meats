#!/usr/bin/env python

import sys

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
 
def createMultiPage(num_pages=5, output="canvas_page_num.pdf"):
    c = canvas.Canvas(output)
    for i in range(num_pages):
        page_num = c.getPageNumber()
        text = "Page %s of %d" % (page_num, num_pages)
        c.drawString(1.5*cm, 2*cm, text) # X axis -> , Y axis |^
        c.showPage()
    c.save()
 
if __name__ == "__main__":
    if len(sys.argv) > 1:
        createMultiPage(int(sys.argv[1]))
    else:
        createMultiPage()
