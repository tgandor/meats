#!/bin/bash

# https://superuser.com/questions/1050155/kde-plasma-partial-screen-after-unplugging-hdmi-second-screen
# https://superuser.com/a/1153184/269542

# Setup utility: kcmshell5 kcm_kscreen

mv $HOME/.local/share/kscreen $HOME/.local/share/`date --iso`-kscreen
read -p "Press Enter to reboot or Ctrl+C to cancel..."
sudo reboot
