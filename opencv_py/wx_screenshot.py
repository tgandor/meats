#!/usr/bin/env python

# https://stackoverflow.com/questions/2846947/get-screenshot-on-windows-with-python
# one of quite a few answers.

from __future__ import print_function

import argparse

import wx

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', default='screenshot.png')
args = parser.parse_args()

app = wx.App()  # Need to create an App instance before doing anything
screen = wx.ScreenDC()
size = screen.GetSize()
print('Screen size:', size)

# bmp = wx.EmptyBitmap(size[0], size[1]) - deprecated
bmp = wx.Bitmap(size[0], size[1])
mem = wx.MemoryDC(bmp)
mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
bmp.SaveFile(args.output, wx.BITMAP_TYPE_PNG)
print('Screenshot saved to:', args.output)

