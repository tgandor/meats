#!/bin/bash

name=${1:-admin}

sudo useradd -M -s /sbin/nologin $name
# Lockdown:
sudo passwd -l $name
# User info:
id $name
