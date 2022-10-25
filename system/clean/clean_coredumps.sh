#!/bin/bash

df -h /var/lib/systemd/coredump/
df /var/lib/systemd/coredump/
sudo rm /var/lib/systemd/coredump/core.*
df /var/lib/systemd/coredump/
df -h /var/lib/systemd/coredump/
