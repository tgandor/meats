
import random
import sys

for line in sys.stdin:
    words = line.split()
    random.shuffle(words)
    print(' '.join(words))

