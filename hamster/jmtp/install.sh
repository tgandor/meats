#!/bin/bash

source=`realpath $1`
pushd `dirname $0`/..
if ! jmtp/mount.sh ; then
	echo "Error: not able to mount phone (nothing installed)"
	exit
fi
cp -v $source mnt/Phone/com.hipipal.qpyplus/scripts/
jmtp/umount.sh
popd
