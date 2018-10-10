# based on: https://stackoverflow.com/a/6076779/1338797

import argparse
import sys

class VAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        print('values: {v!r}'.format(v=values))
        if values==None:
            values='1'
        try:
            values=int(values)
        except ValueError:
            values=values.count('v')+1
        setattr(args, self.dest, values)

parser=argparse.ArgumentParser()
parser.add_argument('-v', nargs='?', action=VAction, dest='verbose')
parser.add_argument('-x', action='store_true', dest='ex')
parser.add_argument('-y', '--why')


def test(in_args):
	print(repr(in_args))
	args=parser.parse_args(in_args)
	print(args)
	print('-' * 10)

test(['-v -v'])

test(['-v -v -v'])

test('-v -v -v'.split())

print('Current args:')
test(sys.argv[1:])
