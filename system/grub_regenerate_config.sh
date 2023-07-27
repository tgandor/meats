#!/bin/bash

# Thanks: https://superuser.com/a/1581482

sudo cp -v /boot/grub/grub.cfg /boot/grub/grub.cfg-pre-`date +%Y-%m-%d_%H%M`
sudo grub-mkconfig -o /boot/grub/grub.cfg
