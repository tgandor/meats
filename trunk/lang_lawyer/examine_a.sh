#!/bin/bash

if [ -z "$1" ] ; then
	echo "Usage: $0 lib<something>.a"
	exit
fi

basename=`basename "$1"`
stem="`dirname "$1"`/$basename"

if [ `basename $1 .a` == $basename ] ; then
	echo "$0: error: $1 seems not a library."
	exit
fi

nm "$1"> "$stem.names"
nm --demangle "$1" > "$stem.filt"
vim -O "$stem.names" "$stem.filt"

