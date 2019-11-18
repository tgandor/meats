<?php echo $_SERVER['HTTP_USER_AGENT'] . "\n\n";

$browser = get_browser(null, true);

if ($browser) {
    echo "<pre>\n";
    echo "Using: " . ini_get('browscap') . "\n";
    print_r($browser);
    echo "</pre>\n";
} else {
    echo "get_browser() returned false. Check browsecap.ini configuration.\n";
}
