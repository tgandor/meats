#!/bin/bash

GB=${1:-10}
FILE=${2:-btrfs.img}
MOUNTPT=${3:-$(basename "$FILE" .img)}
MOUNTPT=$(realpath "$MOUNTPT")

dd if=/dev/zero of=$FILE bs=1G count=$GB status=progress
mkfs.btrfs $FILE
echo "Created btrfs volume $FILE of size $GB GB"
mkdir -p $MOUNTPT
sudo mount -o loop,compress=zstd:15 $FILE $MOUNTPT

echo "You can mount it with:"
echo "  sudo mount -o loop,compress=zstd:15 $FILE $MOUNTPT"
echo "Mounted at $MOUNTPT"
echo "Remember to unmount with:"
echo "  sudo umount $MOUNTPT"

echo "fstab entry suggestion:"
echo "$(realpath $FILE)  $MOUNTPT  btrfs  loop,compress=zstd:15  0  0"
