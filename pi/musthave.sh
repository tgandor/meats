#!/bin/bash

if [ -z  "`find /var/cache/apt/pkgcache.bin -mmin -30`" ] ; then
    sudo apt update
    sudo apt -y upgrade
fi

sudo apt-get install -y \
    htop \
    iftop \
    iotop \
    jq \
    kdesdk-scripts \
    mc \
    mercurial \
    net-tools \
    pipx \
    sqlite3 \
    tmux \
    vim \
    vlc-nox \

pipx ensurepath
pipx install poetry uv

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
