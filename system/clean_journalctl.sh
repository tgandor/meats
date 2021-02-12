#!/bin/bash

df -h /var/log/journal
du -h /var/log/journal
# https://linuxhandbook.com/clear-systemd-journal-logs/
sudo journalctl --rotate
# this leaves more than 1h behind (active files remain intact)
sudo journalctl --vacuum-time=1h
df -h /var/log/journal
du -h /var/log/journal

