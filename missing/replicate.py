#!/usr/bin/env python

import argparse
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('template')
parser.add_argument('listing_file')
parser.add_argument('--words', '-n', type=int,
                    help='Number of words to replace in template using listing file', default=2)
args = parser.parse_args()

if __name__ == '__main__':
    name_parts = args.template.split()
    with open(args.listing_file, encoding='utf8') as f:
        for line in f:
            words = line.split()
            name_parts[:args.words] = words[:args.words]
            target = ' '.join(name_parts)
            if os.path.exists(target):
                print(repr(target), 'exists')
                continue

            shutil.copy(args.template, target)
