#!/bin/bash

# this is a loopback solution, maybe check out this:
# https://docs.oracle.com/cd/E52668_01/E54669/html/ol7-s14-storage.html
# Also, I previously used something like this:
# https://www.techrepublic.com/blog/linux-and-open-source/create-encrypted-loopback-filesystems-on-linux/
# but it's out of date a bit: now there's cryptsetup instead of losetup -e aes

# so finally I went more or less with this:
# https://willhaley.com/blog/encrypted-file-container-disk-image-in-linux/

if [ -z "$2" ] ; then
    gb=10
else
    gb=$2
fi

if [ -z "$1" ] ; then
    file=image_.bin
else
    file="$1"
fi

if [ -f $file ] ; then
    echo "File '$file' exists. Please use open_safer_volume.sh $file."
    exit
fi

# echo "Generating $gb GB image... (this may take some time)"
# dd if=/dev/urandom of=$file bs=1G count=$gb iflag=fullblock

# wow, this is quite safe, and won't actually destroy $file accidentally
dd if=/dev/zero of=$file bs=1G count=0 seek=$gb

sudo cryptsetup luksFormat $file --use-urandom

echo "Opening file as /dev/mapper/$file"
sudo cryptsetup open $file $file

echo "Formatting /dev/mapper/$file as ext4"
sudo mkfs.ext4 /dev/mapper/$file

echo "Preparing mount point /mnt/$file"
sudo mkdir /mnt/$file

me=`whoami`
echo "Mounting for user $me"
sudo mount /dev/mapper/$file /mnt/$file
sudo chown $me /mnt/$file
