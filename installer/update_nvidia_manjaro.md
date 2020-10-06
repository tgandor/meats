# The inconvenient truth

To do it without restarting, you have to succeed in the change. Otherwise,
you may reboot to a black screen.

Remove the old nvidia-utils and nvidia driver:

```
# sudo pacman -Rdd nvidia-440xx-utils linux54-nvidia-440xx
# sudo pacman -S nvidia-utils
# sudo pacman -S linux54-nvidia-450xx
```

The second line gives a choice of the nvidia utils version.
It could also spell `sudo pacman -S nvidia-450xx-utils`.

Forgetting the last line can also leave you with a black screen.

Also, the name prefix `linux54` depends on your Kernel version.

Now reboot and hope for the best.

# Everything below is BS

Unfortunately.

First - if you have a text session, you may not have WiFi (NetworkManager...)
It's possible to connect manually with iwconfig/whatever, but it's a pain.

And mhwd will simply try to install the above manually, but can fail because of conflicts
(e.g. CUDA - if it's installed and depends on the driver).

## Log in to text session

E.g. like [here](https://www.linuxuprising.com/2020/01/how-to-boot-to-console-text-mode-in.html):

a. hold Shift
b. keep pressing Esc

then - select the option and press `e`.

add `<space>3` at the end.

# Run mhwd to update the driver

E.g. for driver 450 (like [here](https://forum.manjaro.org/t/installing-nvidia-450-xx-drivers-after-2020-08-22-stable-update/11873/15)):

```
sudo mhwd -i pci video-nvidia-450xx
```

