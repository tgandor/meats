#!/bin/bash

FILE=${1:-btrfs.img}
GB=${2:-100}
MOUNTPT=${3:-$(basename "$FILE" .img)}
MOUNTPT=$(realpath "$MOUNTPT")

if ! grep -q btrfs /proc/filesystems; then
    echo "btrfs is not supported on this system. Please install btrfs-progs and ensure the kernel supports btrfs."
    exit 1
fi

if [ -f "$FILE" ]; then
    echo "File $FILE already exists. Please choose a different filename or remove the existing file."
    exit 1
fi

dd if=/dev/zero of=$FILE bs=1G count=0 seek=$GB
mkfs.btrfs $FILE
echo "Created sparse btrfs volume $FILE of size $GB GB"

mkdir -p $MOUNTPT
sudo mount -o loop,compress=zstd:15,nofail $FILE $MOUNTPT
sudo chown $(id -u):$(id -g) $MOUNTPT
echo "Mounted $FILE at $MOUNTPT with zstd compression level 15"
echo "Changed ownership of $MOUNTPT to $(id -un)"

echo "You can mount it with:"
echo "  sudo mount -o loop,compress=zstd:15,nofail $FILE $MOUNTPT"
echo "Mounted at $MOUNTPT"
echo "Remember to unmount with:"
echo "  sudo umount $MOUNTPT"

echo "fstab entry suggestion:"
echo "$(realpath $FILE)  $MOUNTPT  btrfs  loop,compress=zstd:15,nofail  0  0"
