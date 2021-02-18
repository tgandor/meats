import argparse

parser = argparse.ArgumentParser()
parser.add_argument('arg1', nargs='?')
parser.add_argument('arg2', nargs='?')
args = parser.parse_args()

print(args)

# this simply packs from left to right:
"""
$ python argparse_2_optional.py
Namespace(arg1=None, arg2=None)
$ python argparse_2_optional.py a
Namespace(arg1='a', arg2=None)
$ python argparse_2_optional.py a b
Namespace(arg1='a', arg2='b')
"""
