#!/usr/bin/env python

import sys
import os
import multiprocessing
import subprocess

def go(dta):
    cmd, arg = dta
    if cmd.find('ARG') <> -1:
        cmd = cmd.replace('ARG', arg)
    else:
        cmd = " ".join((cmd, arg))
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    return output

def main():
    num_proc = os.getenv('NUM_PROC')
    p = multiprocessing.Pool(int(num_proc) if num_proc else None)
    print "Mapping, please wait..."
    for output in p.imap_unordered(
        go, 
	[ (sys.argv[1], arg) for arg in sys.argv[2:]] 
    ):
	    print output

if __name__ == '__main__': 
    main()

