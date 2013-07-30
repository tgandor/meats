#!/bin/bash

#defaults:

if [ -z "$fro" ] ; then
	fro=cp949
fi
if [ -z "$too" ] ; then
	too=utf-8
fi

echo "Recoding from $fro to $too"

exit

for f in "$@" ; do 
  iconv -f $fro -t $too "$f" > /tmp/`basename $f`
  mv /tmp/`basename $f` $f
done

