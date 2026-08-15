#!/bin/bash

# Thanks: https://superuser.com/a/1581482

old_cfg=/boot/grub/grub.cfg-pre-`date +%Y-%m-%d_%H%M`
sudo cp -v /boot/grub/grub.cfg $old_cfg
echo "Saved grub.cfg as $old_cfg"
sudo grub-mkconfig -o /boot/grub/grub.cfg

read -rp "update-grub now? [y/N] " answer

if [[ "$answer" =~ ^[Yy]$ ]]; then
    sudo update-grub
else
    echo "Run 'sudo update-grub' yourself (maybe mkconfig did it anyway)."
fi
