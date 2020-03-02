#!/bin/bash

# saving last line must be after the matching cases
# credits: https://stackoverflow.com/a/4891430/1338797
pip search $1 | awk '/INSTALLED/ { print result ; print } /LATEST/ { print } { result = $0 } '

