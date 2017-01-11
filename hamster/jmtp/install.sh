#!/bin/bash

pushd `dirname $0`/..
if ! jmtp/mount.sh ; then
	echo "Error: not able to mount phone (nothing installed)"
	exit
fi

target_dir=mnt/*/qpython/scripts3
if [ ! -d $target_dir ] ; then
	target_dir=mnt/*/qpython/scripts
fi
if [ ! -d $target_dir ] ; then
	target_dir=mnt/*/com.hipipal.qpyplus/scripts
fi

if [ ! -d $target_dir ] ; then
	echo "Sorry, scripts directory not found, opening mountpoint"
	mc mnt
	jmtp/umount.sh
	exit
fi

target_dir=`realpath $target_dir`
popd

if [ -z "$1" ] ; then
	which mc &> /dev/null || sudo apt-get install mc
	mc "$target_dir"
else
	cp -v "$@" "$target_dir"
fi

pushd `dirname $0`/..
jmtp/umount.sh
popd
