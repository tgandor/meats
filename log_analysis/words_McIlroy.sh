#!/bin/bash

# https://leancrew.com/all-this/2011/12/more-shell-less-egg/
# this was also mentioned in AoUP, I guess

tr -cs A-Za-z '\n' |
tr A-Z a-z |
sort |
uniq -c |
sort -rn |
sed ${1}q
