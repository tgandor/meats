#!/usr/bin/env python

import argparse
import os
import qrcode
import sys

parser = argparse.ArgumentParser()
parser.add_argument('data')
parser.add_argument('--output', '-o', default='qr_code.png')
args = parser.parse_args()

img = qrcode.make(args.data)
img.convert('RGB').save(args.output)

