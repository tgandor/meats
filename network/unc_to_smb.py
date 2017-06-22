#!/usr/bin/env python

"""
Change UNC path: https://msdn.microsoft.com/en-us/library/gg465305.aspx
(\\host\share\path\file)
to one used by Samba -- a URL
(smb://host/share/path/file)
"""

from __future__ import print_function
import sys


def convert(unc):
    smb = unc.replace('\\\\', 'smb://')
    smb = smb.replace('\\', '/')
    return smb


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(convert(' '.join(sys.argv[1:])))
    else:
        while True:
            line = sys.stdin.readline().strip()
            if not line:
                break
            line = convert(line)
            print(line)
            # print(line.replace(' ', '%20'))
