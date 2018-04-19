#!/bin/bash

if [ -z "$1" ] ; then
    gigs=1
else
    gigs=$1
fi

# don't try this with /dev/random ! it will take forever and fail

for i in `seq 1 $gigs`; do
    echo "Writing gigabyte $i"
    dd if=/dev/urandom of=gigabyte$i.bin count=1024 bs=1048576
done


for i in `seq 1 $gigs`; do
    rm -v gigabyte$i.bin
done

