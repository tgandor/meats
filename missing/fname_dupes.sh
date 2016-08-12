#!/bin/bash

# find files with repeated basenames
# possible to pass switches to `find`, e.g. -type f

find "$@" | xargs -n1 basename | sort | uniq -c | grep -v '^ *1 ' | sort -n
