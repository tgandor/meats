#!/bin/bash

# https://askubuntu.com/a/720466/309037

if timedatectl | grep local | grep yes ; then
    exit
fi

sudo timedatectl set-local-rtc 1

timedatectl | grep local
