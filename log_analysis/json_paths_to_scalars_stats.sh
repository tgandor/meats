#!/bin/bash

# change all array indexes to 0 (and numbers in identifiers also, don't use them)
# when no argument provided, works as a filter.

jq 'paths(scalars) | join(".")' $1 | sed 's/[0-9]\+/0/g' | sort | uniq -c
