#!/usr/bin/env python

from __future__ import print_function, division, absolute_import

import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--modify', '-w', action='store_true')
parser.add_argument('--print', '-p', action='store_true')
parser.add_argument('--rstrip', '-r', action='store_true')
args = parser.parse_args()


dict_key_line = re.compile('^(\s*)\w+:\s*$')
dict_key = re.compile('^(\s*)\w+:')
leading_ws = re.compile('^\s*')


def get_nonempty_line(lines):
    while True:
        number, line = next(lines)
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            return number, line


def join_simple_keys_and_values(filename, verbose=False):
    lines = enumerate(open(filename))
    for number, line in lines:
        if not line.strip() or line.strip().startswith('#'):
            yield line
            continue

        match = dict_key_line.match(line)
        if match:
            if verbose:
                print('Key line:', number + 1, line.rstrip())

            try:
                number_1, next_1 = next(lines)
            except StopIteration:
                yield line
                return

            indent_key = len(match.group(1))
            indent_next_1 = len(leading_ws.match(next_1).group())

            # this was supposed to be an assertion, but there are corner cases
            if indent_next_1 <= indent_key or next_1.lstrip().startswith('-') or not next_1.strip():
                if not next_1.lstrip().startswith('-'):
                    print('WARNING: next line', number_1+1, 'not indented:', next_1)
                yield line
                yield next_1
                continue

            try:
                _, next_2 = next(lines)
            except StopIteration:
                yield line
                yield next_1
                return

            indent_next_2 = len(leading_ws.match(next_2.rstrip()).group())

            if verbose:
                print('  Indents:', indent_next_1, indent_next_2)

            if indent_next_2 < indent_next_1 and dict_key.match(next_1) is None:
                # Dedent
                key_plus_next = line.rstrip() + ' ' + next_1.lstrip()
                if verbose:
                    print('  Joined =>', key_plus_next)
                yield key_plus_next
                # ideally we should unget the next line
                yield next_2
            else:
                # Indent or same level, or sub-object
                yield line
                yield next_1
                yield next_2
        else:
            # no match
            yield line


def main():
    for filename in args.files:
        print('Processing', filename)
        modified = list(join_simple_keys_and_values(filename, args.verbose))
        if args.print:
            for line in modified:
                print(line, end='')
        if args.modify:
            with open(filename, 'wb') as new_yaml:
                for line in modified:
                    new_yaml.write(line if not args.rstrip else line.rstrip() + '\n')
        print('-' * 60)


if __name__ == '__main__':
    main()
