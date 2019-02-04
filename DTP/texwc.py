#!/usr/bin/env python

import sys
import re

data = open(sys.argv[1]).read() if len(sys.argv)>1 else sys.stdin.read()

body = re.search(r"\\begin\{document\}(.*)\\end\{document\}", data, re.DOTALL)

if not body:
    print "Document not found"
    exit()

body = body.group(1)
body_notag = re.sub(r'\\\w+', '', body)

words = len(re.findall(r'\w+', body))
words2 = len(re.findall(r'\w+', body_notag))
chars = len(re.findall(r'\w', body))
chars2 = len(re.findall(r'\w', body_notag))

body_short = re.sub(r'\s+', ' ', body_notag.strip())

print "Total stats:\n"+"-"*10
print ("Words:\t\t\t%d\nWords (no tags):\t\t%d\nWord Characters:\t\t%d\n"
       "Word Characters (no tags):\t%d\nChars with spaces:\t\t%d\n") % (
           words, words2, chars, chars2, len(body_short))

print "Avg word length: %.1f, word count by 5 cpw %d." % (
      chars2/float(words2), chars2/5)

print "-"*10+"\nSection by section\n"+"-"*10
begin = 0
total = 0
while True:
    begin = body.find(r"\section{", begin)
    if begin == -1:
        break
    print body[begin:body.find('}', begin)+1]
    ends = body.find(r"\section{", begin+1)
    body_notag = re.sub(r'\\\w+', '', body[begin:ends])
    # print body_notag.strip()
    words = len(re.findall(r'\w+', body_notag))
    total += words
    print("Words: %3d, total: %3d\n" % (words, total))
    begin += 1
