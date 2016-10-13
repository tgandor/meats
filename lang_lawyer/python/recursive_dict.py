#!/usr/bin/env python

# dictionary points to itself

d = {'abc': 1, 'def': 2}
print(d)
d['ghi'] = {'jkl': 3}
print(d)
d['mno'] = d
print(d)
d['ghi']['pqr'] = d
print(d)

# list - same here

l = [1, 2, 3]
l.append(l)
print(l)
