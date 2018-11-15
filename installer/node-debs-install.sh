#!/bin/bash

# https://github.com/nodesource/distributions

dl=none

if which curl ; then 
    echo Using curl
    dl="curl -sL" 
fi

if [ "$dl"=="none" ] && which wget ; then
    echo Using wget
    dl="wget -q -O-"
fi

if echo $dl | grep none ; then
    echo Missing any downloader: wget or curl.
    exit
fi

$dl https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs

