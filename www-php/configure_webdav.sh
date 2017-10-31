
if [ ! -f /etc/apache2/apache2.conf  ] ; then
	sudo apt-get install -y apache2
fi

if (grep /webdav /etc/apache2/apache2.conf || [ -d /var/www/webdav ] ) ; then
	echo Looks like you have this configured already.
	exit
fi

sudo a2enmod dav_fs

sudo mkdir -p /var/www/webdav/data


passwdfile=/var/www/webdav/passwd.dav

sudo tee -a /etc/apache2/apache2.conf <<EOF

<Directory /var/www/webdav/data/>
		Options Indexes MultiViews
		AllowOverride None
		Order allow,deny
		allow from all
</Directory>

Alias /webdav /var/www/webdav/data

<Location /webdav>
   DAV On
   AuthType Basic
   AuthName "webdav"
   AuthUserFile $passwdfile
   Require valid-user
</Location>

EOF

echo -n Webdav user name:
read username

sudo htpasswd -c $passwdfile $username

sudo chown -R root:www-data /var/www/webdav
sudo chmod 755 /var/www/webdav
sudo chmod 775 /var/www/webdav/data
sudo chmod 640 $passwdfile

sudo service apache2 restart
