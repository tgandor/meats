#!/usr/bin/env python
import subprocess
import sys


if '///' not in sys.argv:
    print """
Usage:
%s command [-options] /// arguments

To run commands in parallel.

Include a triple slash sign (///) between the command and arguments.

""" % (sys.argv[0],)
    exit()


split = sys.argv.index('///')
command = sys.argv[1:split]
files = sys.argv[split+1:]
half = len(files)/2

"""
print command+files[:half]
print command+files[half:]
"""

p2 = subprocess.Popen(command+files[half:])
if len(files[:half]):
    p1 = subprocess.Popen(command+files[:half])
else:
    p1 = p2

p1.wait()
print 'batch 1 finished'
if p1 <> p2:
    p2.wait()
    print 'batch 2 finished'

