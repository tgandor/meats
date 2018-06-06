#!/bin/bash

# https://unix.stackexchange.com/a/392091/98519
# like CrystalDiskMark ;)

if [ -z "$1" ] ; then
    dir=/tmp
else
    dir=$1
fi

file=$dir/fiotest.tmp

fio --loops=5 --size=1000m --filename=$file --stonewall --ioengine=libaio --direct=1 \
  --name=Seqread --bs=1m --rw=read \
  --name=Seqwrite --bs=1m --rw=write \
  --name=512Kread --bs=512k --rw=randread \
  --name=512Kwrite --bs=512k --rw=randwrite \
  --name=4kQD32read --bs=4k --iodepth=32 --rw=randread \
  --name=4kQD32write --bs=4k --iodepth=32 --rw=randwrite
rm -f $file
