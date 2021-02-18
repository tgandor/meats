import argparse

parser = argparse.ArgumentParser()
parser.add_argument('arg1', nargs='?')
parser.add_argument('arg2', nargs='?')
args = parser.parse_args()

print('        ->', args)

# this simply packs from left to right:
"""
$ python argparse_2_optional.py
Namespace(arg1=None, arg2=None)
$ python argparse_2_optional.py a
Namespace(arg1='a', arg2=None)
$ python argparse_2_optional.py a b
Namespace(arg1='a', arg2='b')
"""

# but wait, what about defaults?

parser = argparse.ArgumentParser()
parser.add_argument('arg1', nargs='?', default='a')
parser.add_argument('arg2', nargs='?')
args = parser.parse_args()

print('a, None ->', args)

parser = argparse.ArgumentParser()
parser.add_argument('arg1', nargs='?', default='a')
parser.add_argument('arg2', nargs='?', default='b')
args = parser.parse_args()

print('a, b    ->', args)

parser = argparse.ArgumentParser()
parser.add_argument('arg1', nargs='?')
parser.add_argument('arg2', nargs='?', default='b')
args = parser.parse_args()

print('None, b ->', args)

# left to right by arguments, overriding defaults;
# if out of arguments, apply defaults:
"""
$ python argparse_2_optional.py
        -> Namespace(arg1=None, arg2=None)
a, None -> Namespace(arg1='a', arg2=None)
a, b    -> Namespace(arg1='a', arg2='b')
None, b -> Namespace(arg1=None, arg2='b')
$ python argparse_2_optional.py x
        -> Namespace(arg1='x', arg2=None)
a, None -> Namespace(arg1='x', arg2=None)
a, b    -> Namespace(arg1='x', arg2='b')
None, b -> Namespace(arg1='x', arg2='b')
$ python argparse_2_optional.py x y
        -> Namespace(arg1='x', arg2='y')
a, None -> Namespace(arg1='x', arg2='y')
a, b    -> Namespace(arg1='x', arg2='y')
None, b -> Namespace(arg1='x', arg2='y')
"""
