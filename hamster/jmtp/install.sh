#!/bin/bash

source=`realpath $1`
pushd `dirname $0`/..
if ! jmtp/mount.sh ; then
	echo "Error: not able to mount phone (nothing installed)"
	exit
fi
if [ -z "$1" ] ; then
	mc mnt/Phone/com.hipipal.qpyplus/scripts/
else
	cp -v $source mnt/Phone/com.hipipal.qpyplus/scripts/
fi
jmtp/umount.sh
popd
