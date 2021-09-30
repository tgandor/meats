#!/bin/bash

dir=`echo $1 | sed 's/ /_/g'`
echo "$1 -> $dir"
mkdir -p -v $dir
