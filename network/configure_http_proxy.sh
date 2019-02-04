#!/bin/bash

# inspired by: https://www.digitalocean.com/community/tutorials/how-to-use-apache-as-a-reverse-proxy-with-mod_proxy-on-debian-8

if [ ! -f /etc/apache2/apache2.conf  ] ; then
	sudo apt-get install -y apache2
fi

sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2

# TODO: automate, parametrize port and alias

cat <<EOF
Add this to /etc/apache2/sites-available/000-default.conf
inside VirtualHost

    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>

    ProxyRequests Off
    ProxyPreserveHost On
    ProxyPass /alias http://localhost:8080/
    ProxyPassReverse /alias http://localhost:8080/
EOF

