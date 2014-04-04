#!/bin/echo This is for sourcing, not running:

alias g99='gcc -std=c99'
echo "Use 'g99' to compile C99"
alias g11='g++ -std=c++0x'
echo "Use 'g11' to compile C++11"

alias g99s='gcc -std=c99 -Wall -Werror'
echo "Use 'g99s' to compile C99 strict"

alias svni='svn --ignore-externals'
echo "Use 'svni' to ignore externals (st, up)."
