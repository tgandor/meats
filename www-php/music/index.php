<?php
    $version = "v3.4-mi-2025.07.08";
    $title = basename(dirname($_SERVER['PHP_SELF']));
    if (empty($title)) {
        $title = 'Music Index';
    }
    $files = glob('*.{mp3,MP3,m4a,M4A,opus}', GLOB_BRACE);
    natsort($files);
    $files = array_values($files);
    $zipAvailable = class_exists('ZipArchive');

    if ($zipAvailable && isset($_GET['action']) && $_GET['action'] === 'download') {
        $zip = new ZipArchive();
        $zipFileName = "$title.zip";

        if ($zip->open($zipFileName, ZipArchive::CREATE | ZipArchive::OVERWRITE) === TRUE) {
            foreach ($files as $file) {
                $zip->addFile($file, basename($file));
            }
            $zip->close();

            header('Content-Type: application/zip');
            header('Content-Disposition: attachment; filename="' . $zipFileName . '"');
            header('Content-Length: ' . filesize($zipFileName));
            readfile($zipFileName);

            unlink($zipFileName);
            exit;
        } else {
            echo "ZIP-ping failed.";
        }
    }

    $crumbs = array();
    $path = '';
    foreach(explode('/', dirname($_SERVER['SCRIPT_NAME'])) as $dir)
    {
        $path .= "$dir/";
        $crumbs[$path] = $dir;
    }

    $descriptions = array();
    foreach($files as  $i => $music_file)
    {
        $descr_file = pathinfo("$music_file", PATHINFO_FILENAME) . ".txt";
        if (file_exists($descr_file))
        {
            $descriptions[$music_file] = file_get_contents($descr_file);
        }
    }

    $bs = 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css';
    if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/bootstrap.min.css'))
        $bs = '/bootstrap.min.css';
    elseif (file_exists('bootstrap.min.css'))
        $bs = 'bootstrap.min.css';
?><!doctype html>
<!-- <?php echo $version ?> -->
<html lang="en">
  <head>
    <title><?php echo $title ?> - Music Index</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="<?php echo $bs ?>"
        integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4"
        crossorigin="anonymous">

    <style>
    .container {
        width: auto;
        max-width: 1280px;
        padding: 0 15px;
    }
    </style>
  </head>

  <body>
    <div class="container">
        <div class="jumbotron d-none d-md-block">
            <h1><?php echo $title ?></h1>
            <p class="lead" title="<?php echo $version ?>">Showing audio files using HTML5.</p>
        </div>

        <div class="page-header d-block d-md-none">
            <h1><?php echo $title ?></h1>
        </div>

        <div class="row">
            <div class="col-12">
                <p>
                    Path:
<?php foreach($crumbs as $path => $dir): ?>
                    / <a href="<?php echo $path ?>"><?php echo $dir ?: '&#8962;'  ?></a>
<?php endforeach ?>
                </p>
            </div>

            <div class="col-12">
            <form>
                <p>
                    Loop:
                    <input type="radio" name="loop" id="loop_none" checked>
                    <label for="loop_none">None</label>
                    <input type="radio" name="loop" id="loop_one">
                    <label for="loop_one">One</label>
                    <input type="radio" name="loop" id="loop_all">
                    <label for="loop_all">All</label>
                </p>
            </form>
            </div>
        </div>

        <div class="row">
<?php foreach($files as $i => $music_file): ?>
            <div class="col-sm-6 col-md-4 col-lg-3 py-3">
                <p><?php echo $i + 1 ?>. <a href="<?php echo $music_file ?>"><?php echo $music_file ?></a></p>
<?php if (isset($descriptions[$music_file])): ?>
                <p class="small"><?php echo $descriptions[$music_file] ?></p>
<?php endif ?>
                <audio controls="controls" preload="none" id="a_<?php echo $i + 1 ?>">
                    <source src="<?php echo $music_file ?>" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
<?php endforeach ?>

<?php if(count($files) > 10): ?>
            <div class="col-12">
                <p>
                    Path:
<?php foreach($crumbs as $path => $dir): ?>
                    / <a href="<?php echo $path ?>"><?php echo $dir ?: '&#8962;'  ?></a>
<?php endforeach ?>
<?php if ($zipAvailable): ?>
                    <a href="?action=download" class="btn btn-primary">Download as ZIP</a>
<?php else: ?>
                    <span class="text-muted">(ZIP download not available)</span>
<?php endif ?>
                </p>
            </div>
<?php endif ?>
        </div>
    </div>

    <script>
    /* https://stackoverflow.com/questions/2551859/html-5-video-or-audio-playlist */
    const n = <?php echo count($files) ?>;
    const audios = document.getElementsByTagName('audio');
    function make_onended(i)
    {
        return function() {
            if ( document.getElementById('loop_one').checked ) {
                audios[i].play();
            } else if ( document.getElementById('loop_all').checked ) {
                audios[(i+1)%n].play();
                window.setTimeout(() => {
                    audios[(i+1)%n].parentElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    window.location.hash = "a_" + (i + 1);
                }, timeout = 200);
            }
        }
    }
    for (let i=0; i<n; ++i)
    {
        audios[i].onended = make_onended(i);
    }
    </script>
  </body>
</html>
