#!/bin/bash

# this is not guaranteed to work at all 
# just playing with unix tools like it's 1999

grep -ar "Count " . | sort | perl -lne 'if(/Count (\d)/) { $sum += $1; print("$_, \n added $1, total: $sum"); }'
