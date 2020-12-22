
d1 = {'a': 1, 'b': 2}
d2 = {'b': 2, 'a': 1}

assert d1 == d2
print(d1 == d2)

a = [1, 2, 3, 1, 2, 3]
b = [3, 2, 1, 3, 2, 1]

ad = [{'a': x} for x in a]
bd = [{'a': x} for x in b]

# https://stackoverflow.com/questions/7828867/how-to-efficiently-compare-two-unordered-lists-not-sets-in-python

# assert sorted(ad) == sorted(bd)
# TypeError: '<' not supported between instances of 'dict' and 'dict'

assert sorted(ad, key=repr) == sorted(bd, key=repr)
print(sorted(ad, key=str) == sorted(bd, key=str))

