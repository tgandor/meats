#!/bin/bash

sshfs -oHostKeyAlgorithms=+ssh-dss "$@"
