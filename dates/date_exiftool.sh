#!/bin/bash

exiftool -CreateDate -csv "$@"
