#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import re

TABU = [
    '/.git',
    '/.hg',
    '/.svn',
    '/.idea',
    '/.vscode',
    '/.ipynb_checkpoints',
    '/__pycache__',
]


def is_directory_tabu(dirpath):
    dirpath = dirpath.replace('\\', '/')
    return any(tabu + '/' in dirpath or dirpath.endswith(tabu) for tabu in TABU)


EXLUCDED = [
    '.avi',
    '.exe',
    '.gz',
    '.h5',
    '.jpeg',
    '.jpg',
    '.json', # questionable, but often they don't have EOL at EOF
    '.md',
    '.mkv',
    '.mp4',
    '.o',
    '.otf',
    '.out', # a.out ...
    '.pdf',
    '.png',
    '.ttf',
]


def is_excluded(filename):
    _, ext = os.path.splitext(filename.lower())
    return ext in EXLUCDED or ext in (args.exclude or ())


LF = b'\n'
CRLF = b'\r\n'


def identify_eol(line):
    if line.endswith(CRLF):
        eol = CRLF
        base_line = line[:-2]
    elif line.endswith(LF):
        eol = LF
        base_line = line[:-1]
    else:
        eol = None
        base_line = line
    return base_line, eol


parser = argparse.ArgumentParser()
parser.add_argument('--crlf', '-w', action='store_true')
parser.add_argument('--fix', '-f', action='store_true')
parser.add_argument('--list', '-l', action='store_true')
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--exclude', '-x', nargs='*', help='exclude files by extension')
parser.add_argument('directory', nargs='?', default='.')
args = parser.parse_args()

def report(message='', *_):
    if args.list:
        return
    print('{}:{}: {} {}'.format(
        path,
        idx+1,
        base_line.replace(b' ', b'.').replace(b'\t', b'--->'),
        message
    ))


def fix_file(path):
    # maybe write an in-place version some day
    lines = []
    prev_eol = None
    for line in open(path, 'rb'):
        base_line, eol = identify_eol(line)
        base_line = base_line.rstrip()

        if args.crlf:
            eol = LF
        elif prev_eol is not None:
            eol = prev_eol

        lines.append(base_line + eol)
        prev_eol = eol

    with open(path, 'wb') as fixed_file:
        fixed_file.write(b''.join(lines))


problem_files = 0
total_problems = 0
total_files = 0

for dirpath, dirnames, filenames in os.walk(args.directory):
    if is_directory_tabu(dirpath):
        continue

    if args.verbose:
        print('Processing directory:', dirpath)

    for filename in filenames:
        if is_excluded(filename):
            continue

        total_files += 1
        if args.verbose:
            print('Processing file:', filename)

        path = os.path.join(dirpath, filename)
        file_eol = None
        problems = 0

        for idx, line in enumerate(open(path, 'rb')):
            base_line, eol = identify_eol(line)

            if eol is None:
                report('No newline at EOF:', path, idx+1)
                problems += 1
            elif file_eol is None:
                file_eol = eol
                if args.verbose:
                    print('File eol', repr(file_eol))
            elif eol != file_eol:
                report('Mixed EOL sequence', path, idx+1)
                problems += 1

            if args.crlf and eol == CRLF:
                report('Windows EOL sequence (CRLF) used', path, idx+1)
                problems += 1

            # check trailing space
            if base_line.rstrip() != base_line:
                report()
                problems += 1

        if problems:
            problem_files += 1
            total_problems += problems
            if not args.list:
                print(problem_files, '-' * 60)
            else:
                print('{} {}: {} problem(s)'.format(problem_files, path, problems))

            if args.fix:
                fix_file(path)

print('Found {} problems in {} of {} examined files.'.format(total_problems, problem_files, total_files))
