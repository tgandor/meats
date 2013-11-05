#!/bin/bash

if which lzip > /dev/null
then
	comp="lzip -9"
elif which bzip2 > /dev/null
then
	comp="bzip2"
else
	comp="gzip -9"
fi

echo "Using '$comp' for compression"

find -maxdepth 1 -mindepth 1 -type d -not -name '.*' | while read d
do
	echo Compressing: $d
	tar cf $d.tar $d
	$comp $d.tar
	rm -r $d
done
