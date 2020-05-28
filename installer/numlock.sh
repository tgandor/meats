#!/bin/bash

# This doesn't work.
# NumLock just still is not on by default...
# BTW, adding `numlockx` to $HOME/.xinitrc is also useless.
# So this is still an open research problem ;)

if ! grep -Hn numlockx /etc/X11/xinit/xinitrc ; then
    echo if "which numlockx ; then numlockx ; fi" | sudo tee -a /etc/X11/xinit/xinitrc
fi

