#!/bin/bash

target=$1

if [ -z "$target" ] ; then
    echo "Usage: $0 <binary_file>"
    exit
fi

if [ ! -f "$target" ] ; then
    target=`which "$target"`
fi

if [ -z "$target" ] ; then
    echo "$target - binary file not found"
    exit
fi

echo "------------------"

echo "Method 1 (overkill): objdump -x"
objdump -x "$target"

echo "------------------"

echo "Method 2: readelf -d"
readelf -d "$target"

echo "------------------"

echo "Method 3: ldd"
ldd "$target"

echo "------------------"

