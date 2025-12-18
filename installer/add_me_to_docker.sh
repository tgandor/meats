#!/bin/bash

if ! which docker &> /dev/null ; then
    echo "Docker not found. Please install docker first."
    exit
fi

if ! groups $USER | grep -q '\bdocker\b' ; then
    echo "Adding $USER to docker group (sudo required)"
    sudo usermod -a -G docker $USER
    echo "Now re-login and run 'id' or 'groups' (or 'docker ps')."
else
    echo "$USER is already in the docker group."
fi
