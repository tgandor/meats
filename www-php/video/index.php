<?php
    $version = "v1.1-vi-2025.07.04";
    $title = basename(dirname($_SERVER['PHP_SELF']));
    if (empty($title)) {
        $title = 'Video Index';
    }
    $files = glob('*.{mp4,webm}', GLOB_BRACE);
    natsort($files);
    $files = array_values($files);

    $crumbs = array();
    $path = '';
    foreach(explode('/', dirname($_SERVER['SCRIPT_NAME'])) as $dir)
    {
        $path .= "$dir/";
        $crumbs[$path] = $dir;
    }

    $descriptions = array();
    foreach($files as  $i => $video_file)
    {
        $descr_file = pathinfo("$video_file", PATHINFO_FILENAME) . ".txt";
        if (file_exists($descr_file))
        {
            $descriptions[$video_file] = file_get_contents($descr_file);
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
    <title><?php echo $title ?> - Video Index</title>
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
            <p class="lead" title="<?php echo $version ?>">Showing video files using HTML5.</p>
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
<?php foreach($files as $i => $video_file): ?>
            <div class="col-12 py-3">
                <p><?php echo $i + 1 ?>. <a href="<?php echo $video_file ?>"><?php echo $video_file ?></a></p>
<?php if (isset($descriptions[$video_file])): ?>
                <p class="small"><?php echo $descriptions[$video_file] ?></p>
<?php endif ?>
                <video controls="controls" preload="none" id="a_<?php echo $i + 1 ?>">
                    <source src="<?php echo $video_file ?>" type="video/mp4">
                    Your browser does not support the video element.
                </video>
            </div>
<?php endforeach ?>

<?php if(count($files) > 10): ?>
            <div class="col-12">
                <p>
                    Path:
<?php foreach($crumbs as $path => $dir): ?>
                    / <a href="<?php echo $path ?>"><?php echo $dir ?: '&#8962;'  ?></a>
<?php endforeach ?>
                </p>
            </div>
<?php endif ?>
        </div>
    </div>

    <script>
    /* https://stackoverflow.com/questions/2551859/html-5-video-or-audio-playlist */
    const n = <?php echo count($files) ?>;
    const videos = document.getElementsByTagName('video');
    function make_onended(i)
    {
        return function() {
            if ( document.getElementById('loop_one').checked ) {
                videos[i].play();
            } else if ( document.getElementById('loop_all').checked ) {
                videos[(i+1)%n].play();
                window.setTimeout(() => {
                    videos[(i+1)%n].scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }, timeout = 1000);
            }
        }
    }
    for (let i=0; i<n; ++i)
    {
        videos[i].onended = make_onended(i);
    }
    </script>
  </body>
</html>
