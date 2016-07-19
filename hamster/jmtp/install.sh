#!/bin/bash

source=`realpath $1`
pushd `dirname $0`/..
jmtp/mount.sh
cp -v $source mnt/Phone/com.hipipal.qpyplus/scripts/
popd