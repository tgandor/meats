
class enumenum(type):
    def __new__(mcs, name, bases, dict):
        print "Metaclass called:", name
        print "Bases:", bases
        print "Dict:", dict
        print '-'*50
        dict['items'] = sorted(k for k in dict.keys() if not k.startswith('_'))
        return type.__new__(mcs, name, bases, dict)

class Enum(object):
    __metaclass__ = enumenum

class Statuses(object):
    new = 0
    medium = 1
    old = 2

print Statuses.medium

class Interpolations(Enum):
    NN = 0
    Bilinear = 1
    Bicubic = 2

for val in Interpolations.items:
    print val
