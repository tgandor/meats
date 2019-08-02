#!/bin/bash

# https://superuser.com/questions/387007/equivalent-echo-on-for-linux

# Note: these options (-x, -v) can be also added to shebang, like:
#!/bin/bash -v

# echo on, itself not echoed
set -x
sleep 1
sleep 2
sleep 3
# echo off, itself echoed
set +x
echo done -x

# a different echo - reports lines, not every step in a pipe, no '+' prefix
set -v
sleep 1
sleep 2
set +v
echo done -v
