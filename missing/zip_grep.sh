#!/bin/bash

# wcgrep ideas?

pattern=$1
shift 1

for i in "$@"; do
    zipgrep $pattern "$i"
done
