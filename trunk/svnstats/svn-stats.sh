#!/bin/bash

svn log $LOGURL | awk '/^r[1-9]/ { print $3; }' | sort | uniq -c | sort -n
