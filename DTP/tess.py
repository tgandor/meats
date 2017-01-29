#!/usr/bin/env python

"""
Script for calling tesseract with output == basename+'.txt' for each argument.

Some protection against overwriting existing files.
"""

from __future__ import print_function

import os
import subprocess
import sys


def main():
    """Main function."""
    for image in sys.argv[1:]:
        basename, _ = os.path.splitext(image)

        if os.path.exists(basename + '.txt'):
            print('Skipping {} - {} exists.'.format(image, basename+'.txt'))
            continue

        subprocess.call(['tesseract', image, basename])

if __name__ == '__main__':
    main()
