#!/bin/bash

echo "Installing neccessary build tools"
sudo apt install build-essential flex bison dwarves libssl-dev libelf-dev cpio

echo
if [ "$(basename $(pwd))" !=  "WSL2-Linux-Kernel" ] ; then
    echo "Cloning huge kernel repo..."
    time git clone https://github.com/microsoft/WSL2-Linux-Kernel.git
    cd "WSL2-Linux-Kernel"
fi

echo "Configuring the build"
make menuconfig KCONFIG_CONFIG=Microsoft/config-wsl

echo "Probably confiugred, now run:"
echo "(but wait, edit the KCONFIG_CONFIG and replace all =m with =y)"
echo "time make -j$(nproc) KCONFIG_CONFIG=Microsoft/config-wsl"
echo "And then, maybe:"
echo "sudo make modules_install"
echo "[sudo] cp arch/x86/boot/bzImage /mnt/c/Users/<YourUsername>/bzImage"
