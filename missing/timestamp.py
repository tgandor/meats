
import argparse
import glob
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+', help='Files to timestamp')
parser.add_argument('--write', '-w', action='store_true', help='Append comment to files')
parser.add_argument('--comment', '-c', help='Comment prefix', default='#')
args = parser.parse_args()

for f in (g for arg in args.files for g in glob.glob(arg)):
    mtime = os.path.getmtime(f)
    date = time.strftime("%Y-%m-%d (%A) %H:%M:%S", time.localtime(mtime))
    print(f, date)
    if args.write:
        with open(f, 'a') as output:
            output.write('\n{} last modified: {}\n'.format(args.comment, date))
