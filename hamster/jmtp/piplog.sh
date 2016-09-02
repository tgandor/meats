#!/bin/bash

source="mnt/Phone/Download/pip.log"
target=`pwd`
pushd `dirname $0`/..
jmtp/mount.sh
cp -v $source $target
jmtp/umount.sh
popd
