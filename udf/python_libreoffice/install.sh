#!/bin/bash

sudo apt install libreoffice-script-provider-python

deploy() {
    if [ -f $2/$1 ] ; then
        echo $1 Seems already installed in $2
    else
        sudo cp `dirname $0`/$1 $2
    fi
}

mkdir -p ~/.config/libreoffice/4/user/Scripts/python

deploy CurrentDate.py ~/.config/libreoffice/4/user/Scripts/python
# deploy CurrentDate.py /usr/lib/libreoffice/share/Scripts/python

