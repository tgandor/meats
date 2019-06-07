#!/bin/bash

# Just like that ;)

if which apache2ctl &>/dev/null ; then
    if apache2ctl -M &>/dev/null ; then
        apache2ctl -M 2>/dev/null | grep -v Loaded | sort -b
    else
        sudo apache2ctl -M 2>/dev/null | grep -v Loaded | sort -b
    fi
else
# BTW, instalation of PHP in Manjaro is a bit manual, no a2enmod and a2dismod
# to switch to prefork etc., see here:
# https://wiki.archlinux.org/index.php/Apache_HTTP_Server#PHP
    if apachectl -M &>/dev/null ; then
        apachectl -M 2>/dev/null | grep -v Loaded | sort -b
    else
        sudo apachectl -M 2>/dev/null | grep -v Loaded | sort -b
    fi
fi

