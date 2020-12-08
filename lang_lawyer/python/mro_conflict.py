# this example comes from the Python article:
# https://www.python.org/download/releases/2.3/mro/
# by Michele Simionato

# key ideas:
# - linearization = MRO
# - L[C(B1 .. BN)] = C + merge(L[B1], ..., L[BN], B1..BN)
#                                                 ^^^^^^  - super important!

F = type('Food', (), {'remember2buy': 'spam'})
E = type('Eggs', (F,), {'remember2buy': 'eggs'})
try:
    G = type('GoodFood', (F, E), {})
except TypeError as te:
    print(te)

# Discussion:
# L[G] = G + merge(FO, EFO, FE)
# E = bad head because of FE
# F = bad head because of EFO

class F1: remember2buy = 'spam'
class E1(F1): remember2buy = 'eggs'
class G1(E1, F1): pass

# Discussion:
# L[G1] = G1 + merge(E1 F1 O, F1 O, E1 F1)
# E1 = good head (not in any tail)
# L[G1] = G1 E1 + merge(F1 O, F1 O, F1)
# F1 = good head ()
# L[G1] = G1 E1 F1 + merge(O, O, [])
# O = good "head" (tail)
# L[G1] = G1 E1 F1 O

print('G1 buys:', G1.remember2buy)

# Homework: watch "Super considered super" by R. Hettinger
