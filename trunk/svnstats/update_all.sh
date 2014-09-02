#!/bin/bash

for f in */.svn ; do
# this was too slow, really:
# find -type d -name .svn | while read f; do
	directory=`dirname $f`
	# if [ ! -d $f/../../.svn ] ; then
		echo "*** Updating $directory ***"
		svn up "$directory"
	# fi
done

