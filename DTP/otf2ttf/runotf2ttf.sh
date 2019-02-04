#!/bin/bash

for i in *.otf; do fontforge -script otf2ttf.ff $i; done

