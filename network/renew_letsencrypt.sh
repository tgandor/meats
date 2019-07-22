#!/bin/bash

if [ ! -f ./certbot-auto ] ; then
    wget https://dl.eff.org/certbot-auto
    chmod +x certbot-auto
fi

sudo ./certbot-auto renew

# For nginx
sudo bash -c "cp /etc/letsencrypt/live/*/fullchain.pem /etc/nginx/cert.crt"
sudo bash -c "cp /etc/letsencrypt/live/*/privkey.pem /etc/nginx/cert.key"
