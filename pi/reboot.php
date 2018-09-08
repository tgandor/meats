<?php
// Modifierd from: http://www.raspberry-projects.com/pi/software_utilities/web-servers/php-code-bits/reboot

//----- DO THE REBOOT -----
// THIS SUDO COMMAND NEEDS TO BE AUTHORISED FOR APACHE TO USE IT IN THE FILE:
// sudo visudo
//	# Special for this system - let apache run exes we use in the web interface
//	www-data ALL=NOPASSWD: /sbin/reboot
	echo '<pre>';
	system("(sleep 2 ; sudo /sbin/reboot ) > /dev/null 2>&1 & echo $!");
	echo '</pre>';


