#!/bin/bash

if [ "$1" == "" ] ; then
    pamac build visual-studio-code-bin
else
    [ -d visual-studio-code-bin ] || git clone https://aur.archlinux.org/visual-studio-code-bin.git
    cd visual-studio-code-bin
    makepkg -s
    mv visual-studio-code-bin*.pkg.tar.zst ..
    git clean -dfx
fi
