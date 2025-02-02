#!/bin/bash

# git is already there, I guess

sudo apt install -y "$@" \
    curl \
    fdupes \
    ffmpeg \
    htop \
    iotop \
    ipython3 \
    kdesdk-scripts \
    lm-sensors \
    mc \
    net-tools \
    python3-pip \
    python3-poetry \
    python3-virtualenv \
    python-is-python3 \
    rar \
    sqlite3 \
    tmux \
    vim \
    zip \
# end.

sudo ln -sf /usr/bin/ipython3 /usr/bin/ipython
