#!/usr/bin/env python

"""
Script for calling tesseract with output == basename+'.txt' for each argument.

Some protection against overwriting existing files.
"""

from __future__ import print_function

import argparse
import os
import subprocess


def main():
    """Main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', '-l', help='Language to use')
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()

    base_command = ['tesseract']
    if args.lang:
        base_command.extend(['-l', args.lang])

    for image in args.files:
        basename, _ = os.path.splitext(image)

        if os.path.exists(basename + '.txt'):
            print('Skipping {} - {}.txt exists.'.format(image, basename))
            continue

        print('OCR-ing {} to {}.txt ...'.format(image, basename))
        print(base_command + [image, basename])
        subprocess.call(base_command + [image, basename])
        print('-'*40)

if __name__ == '__main__':
    main()
