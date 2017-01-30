<?php 

$cwd = ($_SERVER['HTTPS'] ? 'https://' : 'http://') . $_SERVER['HTTP_HOST'] . dirname($_SERVER['PHP_SELF']);
$dir_base = basename($cwd);

if ($_GET['show'])
{
    header('Content-Type: text/plain');
    echo "File: $dir_base.m3u\n";
}
else
{
    header('Content-Type: audio/x-mpegurl');
    header("Content-Disposition: attachment;filename=$dir_base.m3u");
}

foreach (glob('*.mp3') as $fn)
{
    echo str_replace(' ', '%20', "$cwd/$fn\n");
}
