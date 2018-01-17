#!/bin/bash

if [ -z "$1" ] ; then
    echo "Usage: $0 user@host [-p port etc.]"
    echo "Adds id_rsa.pub (generates if missing) to user's .ssh/authorized_keys"
    exit
fi

if [ ! -f $HOME/.ssh/id_rsa ] ; then
    echo "Generating Keys, press enter a couple of times..."    
    ssh-keygen
fi

if ( ssh -o PasswordAuthentication=no $* pwd ) ; then
    echo "You are already authorized!"
    exit
fi

cat $HOME/.ssh/id_rsa.pub | ssh $* "mkdir -p .ssh ; tee -a .ssh/authorized_keys"

if ( ssh -o PasswordAuthentication=no $* pwd ) ; then
    echo "Success!"
else
    echo "Something doesn't work. Change to 0600?"
fi
