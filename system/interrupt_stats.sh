#!/bin/bash

# Some interrupts eating your battery? Check what they are:
# https://unix.stackexchange.com/questions/398520/kworker-consumes-high-cpu-for-external-hard-drive
# this is a nice abuse of grep, to print filenames and their content on a single line:
# grep . -r /sys/firmware/acpi/interrupts/

# but we want to sort it right away, so...

for int in /sys/firmware/acpi/interrupts/* ; do echo `cat $int` $int ; done | sort -n | grep -v ^0

# See also:
# https://forum.manjaro.org/t/kworker-kacpid-cpu-100/131532
# perf record -g -a sleep 10
# perf report

echo "Now, for example:"
echo "echo disable | sudo tee /sys/firmware/acpi/interrupts/gpe6F"

