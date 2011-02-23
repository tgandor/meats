#!/usr/bin/env python

import sys
import os
import multiprocessing
import subprocess

def go(dta):
    cmd, arg = dta
    cmd = cmd.replace('ARG', arg)
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    return output

def main():
    p = multiprocessing.Pool()
    print "Mapping, please wait..."
    outputs = p.map(go, [ (sys.argv[1], arg) for arg in sys.argv[2:]] )
    print "\n".join(outputs)

if __name__ == '__main__': main()

