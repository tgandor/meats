#!/bin/bash

if [ -z  "`find /var/cache/apt/pkgcache.bin -mmin -30`" ] ; then
    sudo apt update
    sudo apt -y upgrade
fi

sudo apt-get install -y \
    aptitude \
    htop \
    kdesdk-scripts \
    mc \
    python3 \
    python3-pip \
    python-pip \
    screen \
    tmux \
    vim \
    vlc-nox \

if [ ! -e $HOME/.bash_aliases ] ; then
    echo Creating $HOME/.bash_aliases
    tee $HOME/.bash_aliases <<EOF
alias ll='ls -l'
alias la='ls -A'
alias l='ls -CF'
EOF
fi

if [ ! -e $HOME/.vimrc ] ; then
    echo Creating $HOME/.vimrc
    cp `dirname $0`/../configs/.vimrc $HOME
    # the default colors on RPi are too dark on comments:
    echo "colorscheme torte" >> $HOME/.vimrc
fi
