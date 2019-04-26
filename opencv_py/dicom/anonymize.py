#!/usr/bin/env python

# Consider also:
# http://manpages.ubuntu.com/manpages/xenial/man1/dcmodify.1.html

from __future__ import print_function

import argparse
import glob
import os

try:
    import pydicom
except ImportError:
    print('Missing pydicom')
    print('pip install pydicom')
    exit()


def gen_files(args):
    for item in args.files_dirs_globs:
        if os.path.isfile(item):
            yield item
        elif os.path.isdir(item):
            for dirpath, _, filenames in os.walk(item):
                for filename in filenames:
                    yield os.path.join(dirpath, filename)
        elif '**' in item:
            # will fail in 2.7
            for filename in glob.glob(item, recursive=True):
                yield filename
        else:
            for filename in glob.glob(item):
                yield filename


parser = argparse.ArgumentParser()
parser.add_argument('files_dirs_globs', nargs='+')
parser.add_argument('--backup', '-b', action='store_true')
args = parser.parse_args()

for filename in gen_files(args):
    print('Processing', filename)
    dataset = pydicom.dcmread(filename)

    # minor hack:
    # DICOM: https://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/DICOM.html
    # knows nothing about it...
    if (0x0010, 0x9910) in dataset:
        print('removing unknown item 0x0010, 0x9910')
        del dataset[0x0010, 0x9910]
    # end hack

    # this failed previously with 'Unknown DICOM tag'...
    dataset.remove_private_tags()

    # cleaning for real:
    for item in list(dataset.keys()):
        # 0x10 - patient group
        if item.group == 0x10:
            print('Removing', item, dataset[item])
            del dataset[item]
        # 0x08 - institution, partially
        elif item.group == 0x08 and 0x80 <= item.element <= 0x90:
            print('Removing', item, dataset[item])
            del dataset[item]

    # Request Attributes Sequence (Physician Name)
    if (0x40, 0x275) in dataset:
        print('Removing', dataset[0x40, 0x275])
        del dataset[0x40, 0x275]

    if args.backup:
        os.rename(filename, filename + '.bak')

    pydicom.dcmwrite(filename, dataset)
