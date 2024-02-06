#!/bin/bash

du -h ~/.cache/thumbnails/
rm ~/.cache/thumbnails/normal/*
rm ~/.cache/thumbnails/large/*
rm ~/.cache/thumbnails/x-large/*
rm -rf ~/.cache/thumbnails/xx-large
du -h ~/.cache/thumbnails/
