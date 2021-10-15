#!/usr/bin/env python

import re
import sys

TOO_COMMON = 2

lhs = open(sys.argv[1]).read()
rhs = open(sys.argv[2]).read()

try:
	ngram = int(sys.argv[3])
	if ngram < 1:
		ngram = 1
except:
	ngram = 1

matcher = re.compile(' '.join(['\w+']*ngram), re.UNICODE)

lwords = matcher.findall(lhs)
rwords = matcher.findall(rhs)

common = set(lwords) & set(rwords)

numunique = 0
for w in sorted(common):
	if lhs.count(w) < TOO_COMMON and rhs.count(w) < TOO_COMMON:
		numunique += 1
		print(numunique, w)
