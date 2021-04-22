#!/usr/bin/env python


class Nothing:
    pass


class OnlyStr:
    def __str__(self):
        return 'OnlyStr_str'


class OnlyRepr:
    def __repr__(self):
        return 'OnlyRepr_repr'


class Both:
    def __repr__(self):
        return 'Both_repr'

    def __str__(self):
        return 'Both_str'

print('Prints:')
print(Nothing())
print(OnlyStr())
print(OnlyRepr())
print(Both())

print('Formats: {}, {}, {}, {}'.format(Nothing(), OnlyStr(), OnlyRepr(), Both()))

print('Reprs: {!r}, {!r}, {!r}, {!r}'.format(Nothing(), OnlyStr(), OnlyRepr(), Both()))

