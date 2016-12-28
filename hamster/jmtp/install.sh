#!/bin/bash

source=`realpath $1`
pushd `dirname $0`/..
if ! jmtp/mount.sh ; then
	echo "Error: not able to mount phone (nothing installed)"
	exit
fi

target_dir=mnt/Phone/com.hipipal.qpyplus/scripts
if [ ! -d $target_dir ] ; then
	target_dir=mnt/*/com.hipipal.qpyplus/scripts
fi
if [ ! -d $target_dir ] ; then
	target_dir=mnt/*/qpython/scripts
fi

if [ ! -d $target_dir ] ; then
	echo "Sorry, scripts directory not found, opening mountpoint"
	mc mnt
	jmtp/umount.sh
	exit
fi

if [ -z "$1" ] ; then
	mc $target_dir
else
	cp -v $source $target_dir
fi

jmtp/umount.sh
popd
