#!/bin/bash

if [ -z "$1" ] ; then
	echo "Usage: rep.sh <times> command args..."
	exit
fi

times=$1
shift

for i in `seq 1 $times`; do 
	"$@"
done

