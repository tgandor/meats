#!/usr/bin/env python

# Based on:
# https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-with-ssl-as-a-reverse-proxy-for-jenkins

import os

from six.moves import input

script = """
sudo apt-get update
sudo apt-get install nginx openssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/cert.key -out /etc/nginx/cert.crt
"""

for line in script.strip().split('\n'):
    os.system(line)

domain_name = input('Enter your domain name:')

site_config = """
server {
    listen 81;
    return 301 https://$host:8443$request_uri;
}

server {
    listen 8443;
    server_name """ + domain_name + """;

    ssl_certificate           /etc/nginx/cert.crt;
    ssl_certificate_key       /etc/nginx/cert.key;

    ssl on;
    ssl_session_cache  builtin:1000  shared:SSL:10m;
    ssl_protocols  TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!RC4;
    ssl_prefer_server_ciphers on;

    access_log            /var/log/nginx/redirect.access.log;

    location / {

      proxy_set_header        Host $host;
      proxy_set_header        X-Real-IP $remote_addr;
      proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header        X-Forwarded-Proto $scheme;

      # Fix the “It appears that your reverse proxy set up is broken" error.
      proxy_pass          http://localhost:8080;
      proxy_read_timeout  90;

      proxy_redirect      http://localhost:8080 https://""" + domain_name + """:8443;
    }
}
"""

with open('/etc/nginx/sites-enabled/default', 'w') as config:
    config.write(site_config.strip())

os.system('sudo systemctl restart nginx.service')
