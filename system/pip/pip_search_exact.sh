#!/bin/bash

pip search $1 | awk 'tolower($1) == tolower("'$1'") { i = NR ; print } NR == i+1 && /INSTALLED/ { print } NR == i+2 && /LATEST/ { print }'

