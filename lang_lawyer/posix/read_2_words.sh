#!/bin/bash

echo 1 | while read a b; do echo $a "and" $b ; done
echo 1 2 | while read a b; do echo $a "and" $b ; done
echo 1 2 3 | while read a b; do echo $a "and" $b ; done
# Produces:
# 1 and
# 1 and 2
# 1 and 2 3
