<?php
    $title = basename(dirname($_SERVER['PHP_SELF']));
    // mp3 and m4a, case insensitive (false positives: mpa, m43)
    $files = glob('*.[Mm][Pp4][Aa3]');
    natsort($files);
    $loop = (isset($_GET['loop']) && $_GET['loop'] == 'true');
?><!doctype html>
<html lang="en">
  <head>
    <title><?php echo $title ?> - Music Index</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">

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
            <p class="lead">Showing MP3s as HTML5 audio.</p>
        </div>

        <div class="page-header d-block d-md-none">
            <h1><?php echo $title ?></h1>
        </div>

        <div class="row">
            <div class="col-12">
                <p>
                    Path:
<?php $path = ''; ?>
<?php foreach(explode('/', dirname($_SERVER['SCRIPT_NAME'])) as $i => $dir): ?>
<?php $path .= "$dir/" ?>
                    / <a href="<?php echo $path ?>"><?php echo $dir ? $dir : '&#8962;'  ?></a>
<?php endforeach ?>
                </p>
            </div>
            <div class="col-12">
                <p>
                    Loop: <?php if ($loop): ?> ON <a href="?loop=false">disable</a> <?php else: ?> OFF <a href="?loop=true">enable</a><?php endif ?>

                </p>
            </div>
        </div>

        <div class="row">
<?php foreach($files as $i => $music_file): ?>
            <div class="col-sm-6 col-md-4 col-lg-3 py-3">
                <p><?php echo $i + 1; ?>. <a href="<?php echo $music_file ?>"><?php echo $music_file ?></a></p>
<?php if (file_exists(basename("$music_file", "mp3") . "txt")): ?>
                <p class="small"><?php readfile(basename("$music_file", "mp3") . "txt") ?></p>
<?php endif ?>
                <audio controls="controls" preload="none"<?php if($loop): ?> loop="loop"<?php endif ?>>
                    <source src="<?php echo $music_file ?>" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
<?php endforeach ?>

<?php if(count($files) > 10): ?>
            <div class="col-12">
                <p>
                    Path:
<?php $path = ''; ?>
<?php foreach(explode('/', dirname($_SERVER['SCRIPT_NAME'])) as $i => $dir): ?>
<?php $path .= "$dir/" ?>
                    / <a href="<?php echo $path ?>"><?php echo $dir ? $dir : '&#8962;'  ?></a>
<?php endforeach ?>
                </p>
            </div>
<?php endif ?>
        </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
  </body>
</html>
<!-- Acknowledgements:
* myself (music folder)
* https://getbootstrap.com/docs/4.0/utilities/spacing/ (and other docs)
* Michal Kortas
* kiranvj's answer to: https://stackoverflow.com/questions/37944185/hide-element-for-medium-and-up-devices-bootstrap
-->
