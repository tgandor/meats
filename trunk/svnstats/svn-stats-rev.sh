#!/bin/bash

if [ -z $1 ] ; then
	echo "Usage: $0 REVISION"
	echo "Missing initial revision number"
	exit
fi

svn log -r "$1:HEAD" $LOGURL | awk '/^r[1-9]/ { print $3; }' | sort | uniq -c | sort -n
