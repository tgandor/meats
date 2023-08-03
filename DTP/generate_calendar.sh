#!/bin/bash

output=`date --iso`_calendar.pdf
remind -p12 /dev/null | rem2ps -l -i -e -m A4 | ps2pdf - $output
echo "Generated $output"
xdg-open $output
