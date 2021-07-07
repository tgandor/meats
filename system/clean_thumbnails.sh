#!/bin/bash

du -h ~/.cache/thumbnails/
rm ~/.cache/thumbnails/normal/*
rm ~/.cache/thumbnails/large/*
du -h ~/.cache/thumbnails/
