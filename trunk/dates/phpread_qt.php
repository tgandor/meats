#!/usr/bin/env php
<?php

# This works with (or used to work with):
# http://code.google.com/p/php-reader/

set_include_path(get_include_path().PATH_SEPARATOR.dirname(__FILE__));
require_once("ISO14496.php");

// So called quicktime era
$diff = mktime(0, 0, 0, 1, 1, 1904);

foreach ( $argv as $i => $arg ) {
        if ( !$i ) continue;
	$isom = new ISO14496($arg);
	$date = date("Y-m-d H:i:s", $isom->moov->mvhd->creationTime+$diff);
	echo "$date : $arg\n";
}

