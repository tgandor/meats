
import random
import re

points = 0

while True:
    a, b = sorted([random.randint(1, 10) for _ in xrange(2)], reverse=True)
    while True:
        try:
            ans = raw_input('%d - %d = ? ' % (a, b))
            c = int(ans)
            break
        except EOFError:
            print '\nDo widzenia'
            exit()
        except ValueError:
            print 'Nie rozumiem: "%s"' % (ans,)
    if c == a - b:
        points += 1
        print 'Dobrze! Twoje punkty:', points
    else:
        print 'Niedobrze... to jest: %d' % (a+b,)

