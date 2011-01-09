<?php
  $zf = 'test.zip'; // FILE TO BE PROCESSED - adjust...
  // ZIP handle
  $zh = @zip_open($zf);
  if (!$zh) { die("Zip file <strong>$zf</strong> not opened..."); }
  // Some stats to count sizes etc ;)
  $zipsize = filesize($zf);
  $extrsize = 0;
  // Entry handle
  while ($eh = zip_read($zh)) {
    // Uncompressed file size
    $fs = zip_entry_filesize($eh);
    // File name inside ZIP
    $fn = zip_entry_name($eh);
    // Test if file exists
    if (file_exists($fn)) {
      zip_close($zh);
      die("The file <em>$fn</em> exists! Extraction cancelled. Bye.");
    }
    // Extract
    if ( $fs == 0 ) {
      echo "Creating directory <strong>$fn</strong><br />\n";
      mkdir($fn);
    } else {
      echo "Extracting $fn ($fs bytes)<br />\n";
      // Read file contents
      zip_entry_open($zh, $eh);
      $data = zip_entry_read($eh, $fs);
      zip_entry_close($eh);
      // Write to file (php4's file_put_contents)
      $fh = fopen($fn, 'w');
      fwrite($fh, $data, $fs);
      fclose($fh);
      $extrsize += $fs;
    }
  }
  zip_close($zh);
$ratio = $zipsize * 100 / $extrsize;
$extrsize = number_format($extrsize, 0, ',', ' ');
$zipsize  = number_format($zipsize , 0, ',', ' ');
echo <<<EOF
<hr />
All done! <br />
Extracted size: $extrsize bytes <br />
Compressed size: $zipsize bytes <br />
Compression ratio was: $ratio % <br />
<hr />
EOF;

