#!/bin/bash

time parallel convert -verbose {} {.}.webp ::: "$@"
