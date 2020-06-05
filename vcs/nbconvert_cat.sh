#!/bin/bash

# you may be missing nbdime sometimes

jupyter nbconvert --to python --stdout "$@"
