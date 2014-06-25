#!/bin/bash

#defaults:

if [ -z "$fro" ] ; then
	fro=cp949
fi
if [ -z "$too" ] ; then
	too=utf-8
fi

echo "Recoding from $fro to $too"

for f in "$@" ; do 
  echo $f
  if iconv -f $fro -t $too "$f" > "/tmp/`basename "$f"`"; then
    mv "/tmp/`basename "$f"`" "$f"
  else
    echo "  ... Not overwriting ..."
  fi
done

