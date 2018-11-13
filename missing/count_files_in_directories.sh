#!/bin/bash

# this is also TAoUP-like badness 

find -type f | (while read file ; do echo `dirname $file` ; done) | sort | uniq -c

