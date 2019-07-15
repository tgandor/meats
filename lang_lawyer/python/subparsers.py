from __future__ import print_function
import argparse

"""
I want a CLI with subcommands, having potentially different options,
but the command itself should be optional - i.e. there should be a default.
"""

def info(args):
    print('Info function with args:', args)

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='store_true')


subparsers =  parser.add_subparsers(dest='command', required=False)

# you just watch, what happens when you add a positional global arg AFTER subparsers
# it's quite funny, but doesn't seem useful.
parser.add_argument('base_url', nargs='?')
# if non-optional, it takes precedence over "inner" url argument of the info subparser
# i.e. it is url not base_url that is missing when just 1 arg passed.
# but (!),
# when optional - nargs='?' - it will not be parsed if info is invoked.
# i.e. - the info subparser will have an unexpected argument.

info_parser = subparsers.add_parser('info')
info_parser.add_argument('url')
info_parser.set_defaults(func=info)


args = parser.parse_args()
print('Main got parsed args:', args)

# Conclusions:
# 1. The original idea can't be done at all
# 2. subparsers generally delegate the rest of parsing, don't put anything after them
# 3. for my scenario: I'll just stick with option flags for alternative behaviors.
