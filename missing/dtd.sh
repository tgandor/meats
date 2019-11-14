#!/bin/bash

# Date - time - date: time a command with start and begin.

date | tee .dtd_last
time "$@" 2>&1 | tee -a .dtd_last
date | tee -a .dtd_last

