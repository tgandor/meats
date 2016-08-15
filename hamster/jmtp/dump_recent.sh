#!/bin/bash

if [ -n "$1" ]; then
	target=`realpath "$1"`
else
	target=`pwd`
fi

cd `dirname $0`/..

./jmtp/mount.sh
mv -v mnt/Card/DCIM/Camera/`date +%Y%m%d`* $target
./jmtp/umount.sh
