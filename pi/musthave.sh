#!/bin/bash

sudo apt-get update
sudo apt-get -y upgrade

sudo apt-get install \
    vim \
    python3 \
    htop \
    mc \
    screen \
    tmux \
    python-pip \
    python3-pip \

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
