#!/usr/bin/env python
import sys

if len(sys.argv) < 3:
    print sys.argv, 'Usage: %s limit item1 ... itemN' % sys.argv[0]
    exit()

def search(money_left, item_prices, bag=[]):
    if len(item_prices) == 0:
        yield bag
        return
    current_price = item_prices.pop()
    max_current_count = int(money_left / current_price)
    for i in xrange(max_current_count, 0, -1):
        for result in search(money_left-i*current_price, item_prices[:],
                bag+[(current_price, i)]):
            yield result
    for result in search(money_left, item_prices[:], bag[:]):
        yield result

limit = float(sys.argv[1])
items = sorted(set(map(float, sys.argv[2:])), reverse=True)

for result in search(limit, items):
    print sum(price * count for price, count in result), len(result), sum(count for _, count
            in result), result

