
import re

def isplit(s, splitter=r'\s+', regex=True):
    if not regex:
        splitter = re.escape(splitter)

    start = 0

    for m in re.finditer(splitter, s):
        begin, end = m.span()
        if begin != start:
            yield s[start:begin]
        start = end

    if s[start:]:
        yield s[start:]


_examples = ['', 'a', 'a b', ' a  b c ', '\na\tb ']

def test_isplit():
    for example in _examples:
        assert list(isplit(example)) == example.split(), 'Wrong for {!r}: {} != {}'.format(
            example, list(isplit(example)), example.split()
        )
